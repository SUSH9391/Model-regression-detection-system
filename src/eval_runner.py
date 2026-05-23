from dotenv import load_dotenv
load_dotenv()  # Load environment variables at the top of the file

import asyncio
import json
import os
import time
import uuid
import yaml
from datetime import datetime
from typing import List

from openai import AsyncOpenAI
from src.contracts import TestCase, PromptConfig, EvalResult, RunSummary, EmailAnalysis
from src.diff_engine import calculate_regression_delta, compute_accuracy, load_run_from_file
from src.reporter import generate_report
from src.alerting import send_slack_alert

class EvalEngine:
    def __init__(self, api_key: str | None = None, max_concurrent: int = 10) -> None:
        self.client = AsyncOpenAI(
            api_key=os.getenv("GROQ_API_KEY") or api_key,
            base_url=os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1")
        )
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def evaluate_single_case(self, test_case: TestCase, config: PromptConfig) -> EvalResult:
        async with self.semaphore:
            loop = asyncio.get_event_loop()
            start_time = loop.time()
            model = config.model or os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
            try:
                response = await self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": config.system_prompt + "\n\nYou MUST respond with valid JSON only. No explanation, no markdown, no code fences. Exactly this format: {\"category\": \"billing|technical|account|general\", \"summary\": \"one sentence summary\"}"
                        },
                        {"role": "user", "content": test_case.input_text}
                    ],
                    temperature=config.temperature,
                    max_tokens=200
                )
                latency = loop.time() - start_time
                raw_text = response.choices[0].message.content.strip()
                
                try:
                    parsed_output = EmailAnalysis.model_validate_json(raw_text)
                except Exception:
                    return EvalResult(
                        test_case_id=test_case.id,
                        status="failed",
                        output=None,
                        error=f"JSON parse error: {raw_text[:100]}",
                        metrics={
                            "category_match": 0.0,
                            "latency": latency,
                            "tokens_used": response.usage.total_tokens if response.usage else 0
                        }
                    )

                category_match = 1.0 if parsed_output.category == test_case.expected_category else 0.0
                tokens_used = response.usage.total_tokens if response.usage else 0

                return EvalResult(
                    test_case_id=test_case.id,
                    status="success",
                    output=parsed_output.model_dump(),
                    error=None,
                    metrics={
                        "category_match": category_match,
                        "latency": latency,
                        "tokens_used": tokens_used
                    }
                )
            except Exception as e:
                latency = loop.time() - start_time
                return EvalResult(
                    test_case_id=test_case.id,
                    status="failed",
                    output=None,
                    error=str(e),
                    metrics={
                        "category_match": 0.0,
                        "latency": latency,
                        "tokens_used": 0
                    }
                )

    async def run_suite(self, test_cases: List[TestCase], config: PromptConfig) -> List[EvalResult]:
        print(f"Running {len(test_cases)} test cases...")
        tasks = [self.evaluate_single_case(case, config) for case in test_cases]
        results = await asyncio.gather(*tasks)
        return list(results)

    def save_results(self, results: List[EvalResult], run_summary: RunSummary, path: str) -> None:
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        data = {
            "summary": run_summary.model_dump(mode="json"),
            "results": [r.model_dump(mode="json") for r in results]
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)


async def main() -> None:
    # 1. Load configuration and dataset paths
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Warning: GROQ_API_KEY environment variable is not set. Real API calls will fail.")
        # We still allow execution so GHA workflows or mock tests run without immediately crashing on load
        api_key = "dummy-key"

    prompt_path = os.path.join("prompts", "email_classifier_v1.yaml")
    dataset_path = os.path.join("data", "golden_dataset.json")
    run_log_path = os.path.join("data", "run_log.jsonl")

    # 2. Parse Prompt Config
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_data = yaml.safe_load(f)
    config = PromptConfig(**prompt_data)

    # 3. Parse Golden Dataset
    with open(dataset_path, "r", encoding="utf-8") as f:
        cases_data = json.load(f)
    test_cases = [TestCase(**case) for case in cases_data]

    # 4. Initialize Eval Engine
    engine = EvalEngine(api_key=api_key)

    # 5. Run Evaluation Suite
    results = await engine.run_suite(test_cases, config)

    # 6. Calculate Stats & Summary
    total_tokens = sum(int(r.metrics.get("tokens_used", 0)) for r in results)
    avg_latency = sum(float(r.metrics.get("latency", 0.0)) for r in results) / len(results) if results else 0.0
    accuracy = compute_accuracy(results)
    
    run_id = str(uuid.uuid4())
    branch = os.getenv("BRANCH_NAME", "main")  # Default to main if not specified

    run_summary = RunSummary(
        run_id=run_id,
        prompt_version=config.version_id,
        model=config.model,
        timestamp=datetime.now(),
        accuracy=accuracy,
        avg_latency=avg_latency,
        total_tokens=total_tokens,
        branch=branch
    )

    # Save details of the current run
    current_run_path = os.path.join("data", "runs", f"run_{run_id}.json")
    engine.save_results(results, run_summary, current_run_path)

    # Find baseline: last run tagged branch=main
    baseline_run_path = None
    if os.path.exists(run_log_path):
        with open(run_log_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        log_entry = json.loads(line)
                        if log_entry.get("branch") == "main":
                            baseline_run_path = log_entry.get("run_path")
                    except Exception:
                        pass

    # 7. Diffs against baseline
    baseline_results: List[EvalResult] = []
    baseline_summary = None
    if baseline_run_path and os.path.exists(baseline_run_path):
        try:
            baseline_summary, baseline_results = load_run_from_file(baseline_run_path)
            print(f"Loaded baseline from {baseline_run_path} (accuracy: {baseline_summary.accuracy})")
        except Exception as e:
            print(f"Failed to load baseline file: {e}")

    # Fallback if no baseline exists
    if not baseline_summary:
        print("No baseline run found for branch=main. Using self as baseline (0% delta).")
        baseline_results = results
        baseline_summary = run_summary

    delta = calculate_regression_delta(results, baseline_results)
    print(f"Run completed. Accuracy: {accuracy:.4f} (Baseline: {baseline_summary.accuracy:.4f}, Delta: {delta['accuracy_delta']:.2f}%)")
    print(f"Status: {delta['status'].upper()}, Regressions: {delta['regressions_count']}, Improvements: {delta['improvements_count']}")

    # 8. Append to Global Run Log
    os.makedirs(os.path.dirname(run_log_path), exist_ok=True)
    log_entry = {
        "run_id": run_id,
        "prompt_version": config.version_id,
        "model": config.model,
        "timestamp": run_summary.timestamp.isoformat(),
        "accuracy": accuracy,
        "branch": branch,
        "run_path": current_run_path
    }
    with open(run_log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

    # 9. Generate HTML Report
    report_path = os.path.join("reports", f"report_{run_id}.html")
    generate_report(run_summary, delta, results, report_path)

    # Save latest result metadata for CI integration
    latest_result_path = os.path.join("data", "runs", "latest_result.json")
    with open(latest_result_path, "w", encoding="utf-8") as f:
        json.dump({
            "run_id": run_id,
            "status": delta["status"],
            "accuracy": accuracy,
            "accuracy_delta": delta["accuracy_delta"],
            "regressions_count": delta["regressions_count"],
            "improvements_count": delta["improvements_count"]
        }, f, indent=2)

    # 10. Alert via Slack
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if webhook_url:
        slack_success = send_slack_alert(webhook_url, run_summary, delta, report_path)
        print(f"Slack alert sent: {slack_success}")
    else:
        print("SLACK_WEBHOOK_URL not set. Skipping Slack alert.")

    # 11. Exit with appropriate code if fail status
    if delta["status"] == "fail":
        print("Run status is FAIL. Exiting with non-zero code.")
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())
