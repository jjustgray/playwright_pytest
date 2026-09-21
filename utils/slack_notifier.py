import os
import json
import requests

def send_slack_notification():
    # Retrieve Slack Webhook URL from environment variables
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("SLACK_WEBHOOK_URL variable is missing.")
        return

    # GITHUB_REPOSITORY is automatically set by GitHub Actions as 'owner/repo' (e.g., 'jjustgray/playwright_pytest')
    github_repository = os.getenv("GITHUB_REPOSITORY", "jjustgray/playwright_pytest")
    
    # Parse owner and repo name to construct GitHub Pages URL
    try:
        user_name, repo_name = github_repository.split("/")
    except ValueError:
        print(f"Invalid GITHUB_REPOSITORY format: {github_repository}")
        return

    gh_pages_url = f"https://{user_name}.github.io/{repo_name}/"

    # Construct Slack message payload
    payload = {
        "text": "*Automation Exercise E2E Test Execution Results*",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"🚀 *UI Test Execution Finished!*\n\n📊 *Allure Report*: <{gh_pages_url}|Open GitHub Pages Report>"
                }
            }
        ]
    }

    # Send POST request to Slack Webhook URL
    response = requests.post(
        webhook_url, 
        data=json.dumps(payload),
        headers={'Content-Type': 'application/json'}
    )
    print(f"Slack notification status: {response.status_code}")

if __name__ == "__main__":
    send_slack_notification()