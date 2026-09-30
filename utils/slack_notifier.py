import json
import os
from collections import Counter
from pathlib import Path

import requests

webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
repository = os.environ.get("GITHUB_REPOSITORY")
workflow_status = os.environ.get("WORKFLOW_STATUS", "success")

if not webhook_url:
    print("Error: SLACK_WEBHOOK_URL is not provided.")
    exit(1)

# Формирование ссылки на GitHub Pages
if repository:
    owner, repo_name = repository.split("/")
    gh_pages_url = f"https://{owner}.github.io/{repo_name}/"
else:
    gh_pages_url = "https://github.com"

# Определение статуса для сообщения
status_icon = "🟢 Passed" if workflow_status == "success" else "🔴 Failed"

results_directory = Path(os.environ.get(
    "ALLURE_RESULTS_DIR", "allure-results"))
result_statuses = Counter(
    json.loads(result_file.read_text(encoding="utf-8")
               ).get("status", "unknown")
    for result_file in results_directory.glob("*-result.json")
)

if result_statuses:
    passed_count = result_statuses["passed"]
    failed_count = sum(
        result_statuses[status] for status in ("failed", "broken", "unknown")
    )
    skipped_count = result_statuses["skipped"]
    test_summary = (
        f"{passed_count} passed / {failed_count} failed / "
        f"{skipped_count} skipped"
    )
else:
    test_summary = "unavailable"

payload = {
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    f"*Playwright + Pytest E2E Test Execution*\n"
                    f"*Status:* {status_icon}\n"
                    f"*Results:* {test_summary}"
                )
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"📊 *Allure Report:* <{gh_pages_url}|View Report on GitHub Pages>"
            }
        }
    ]
}

response = requests.post(webhook_url, json=payload)
print(f"Slack Notification Status: {response.status_code}")
