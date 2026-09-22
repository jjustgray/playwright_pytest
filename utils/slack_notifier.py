import os
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

payload = {
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Playwright + Pytest E2E Test Execution*\n*Status:* {status_icon}"
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