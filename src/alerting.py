from dotenv import load_dotenv
load_dotenv()  # Load environment variables at the top of the file

import httpx
from src.contracts import RunSummary

def is_alertable(status: str) -> bool:
    return status.lower() in ("warn", "fail")

def send_slack_alert(
    webhook_url: str,
    run_summary: RunSummary,
    delta: dict,
    report_path: str
) -> bool:
    status = delta.get("status", "pass").lower()
    if not is_alertable(status):
        # We only send if status in ("warn", "fail")
        return False

    status_emojis = {
        "pass": "✅",
        "warn": "⚠️",
        "fail": "🔴"
    }
    emoji = status_emojis.get(status, "❓")
    headline = f"{emoji} Eval Run Complete"

    # Build Slack Block Kit payload
    payload = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": headline,
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Accuracy Delta:*\n{delta.get('accuracy_delta', 0.0)}%"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Regressions:*\n{delta.get('regressions_count', 0)}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Model:*\n`{run_summary.model}`"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Prompt Version:*\n`{run_summary.prompt_version}`"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Report:*\n<{report_path}|View HTML Report> (`{report_path}`)"
                }
            }
        ]
    }

    try:
        response = httpx.post(webhook_url, json=payload, timeout=10.0)
        if response.status_code == 200:
            return True
        else:
            print(f"Slack webhook failed with status code {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"Error sending Slack alert: {e}")
        return False
