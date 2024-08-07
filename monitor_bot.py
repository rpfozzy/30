import requests
import time
import telegram
from github import Github

# Constants
GITHUB_TOKEN = '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'
REPO_NAME = 'rpfozzy/botxxx'
FILE_PATH = 'bot.py'
CHECK_INTERVAL = 1800  # 30 minutes
RECHECK_INTERVAL = 120  # 2 minutes
TELEGRAM_BOT_TOKEN = '6487715421:AAG4WeqsWG_8FkxQbbbZbHDqeDadF-0Ir1g'
ADMIN_CHAT_ID = '1653222949'

# Initialize GitHub and Telegram clients
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

def get_workflow_status():
    url = f"https://api.github.com/repos/{REPO_NAME}/actions/runs"
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    workflows = response.json()['workflow_runs']
    return any(workflow['status'] == 'in_progress' for workflow in workflows)

def update_and_trigger_workflow():
    with open(FILE_PATH, 'r') as file:
        code = file.read()

    contents = repo.get_contents(FILE_PATH)
    repo.update_file(contents.path, "Update bot.py", code, contents.sha)
    repo.create_issue(title="Trigger bot.py", body="Re-triggered bot.py due to inactivity")

def notify_admin(message):
    bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)

def main():
    while True:
        try:
            if not get_workflow_status():
                update_and_trigger_workflow()
                time.sleep(RECHECK_INTERVAL)
                if not get_workflow_status():
                    notify_admin("The bot.py process failed to start.")
                else:
                    print("The bot.py process started successfully.")
            else:
                print("A workflow is currently running.")
        except Exception as e:
            notify_admin(f"An error occurred: {e}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
