import os
import json
from typing import List, Tuple
from src.contracts import EvalResult, RunSummary

def compute_accuracy(results: List[EvalResult]) -> float:
    if not results:
        return 0.0
    matches = [float(r.metrics.get("category_match", 0.0)) for r in results]
    accuracy = sum(matches) / len(results)
    return round(accuracy, 4)

def calculate_regression_delta(current: List[EvalResult], baseline: List[EvalResult]) -> dict:
    current_map = {r.test_case_id: r for r in current}
    baseline_map = {r.test_case_id: r for r in baseline}

    regressions_count = 0
    improvements_count = 0
    regressed_cases = []

    # Match by test_case_id, skipping unmatched IDs gracefully
    for case_id, curr_res in current_map.items():
        if case_id not in baseline_map:
            continue
        base_res = baseline_map[case_id]

        curr_match = float(curr_res.metrics.get("category_match", 0.0))
        base_match = float(base_res.metrics.get("category_match", 0.0))

        if curr_match < base_match:
            regressions_count += 1
            regressed_cases.append({
                "id": case_id,
                "expected_category": curr_res.output.get("category") if curr_res.output else "N/A", # placeholder/default if success but missing
                "baseline_output": base_res.output,
                "current_output": curr_res.output
            })
        elif curr_match > base_match:
            improvements_count += 1

    current_accuracy = compute_accuracy(current)
    baseline_accuracy = compute_accuracy(baseline)
    accuracy_delta = (current_accuracy - baseline_accuracy) * 100.0  # as percentage points

    # Read thresholds from environment variables
    warn_threshold = float(os.getenv("WARN_THRESHOLD", "3.0"))
    fail_threshold = float(os.getenv("FAIL_THRESHOLD", "8.0"))

    # Determine status based on accuracy drop (positive drop value means current is worse than baseline)
    accuracy_drop = -accuracy_delta
    if accuracy_drop < warn_threshold:
        status = "pass"
    elif warn_threshold <= accuracy_drop < fail_threshold:
        status = "warn"
    else:
        status = "fail"

    return {
        "status": status,
        "accuracy_delta": round(accuracy_delta, 2),
        "regressions_count": regressions_count,
        "improvements_count": improvements_count,
        "regressed_cases": regressed_cases
    }

def load_run_from_file(path: str) -> Tuple[RunSummary, List[EvalResult]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    summary = RunSummary(**data["summary"])
    results = [EvalResult(**r) for r in data["results"]]
    return summary, results
