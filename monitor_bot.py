import requests
import telebot
import time

# Настройки
GITHUB_USER = 'rpfozzy'
GITHUB_REPO = 'botxxx'
GITHUB_TOKEN = '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'
TELEGRAM_BOT_TOKEN = '6487715421:AAG4WeqsWG_8FkxQbbbZbHDqeDadF-0Ir1g'
TELEGRAM_CHAT_ID = '1653222949'
CHECK_INTERVAL = 1800  # 30 минут
RETRY_INTERVAL = 120  # 2 минуты

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def send_telegram_message(message):
    bot.send_message(TELEGRAM_CHAT_ID, message)

def get_workflow_runs():
    url = f'https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/actions/runs'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['workflow_runs']

def check_workflows():
    try:
        runs = get_workflow_runs()
        active_runs = [run for run in runs if run['status'] == 'in_progress']
        if active_runs:
            send_telegram_message("1. Гит хаб апи рабочий\n2. Бот работает (процесс активирован)")
            return True
        else:
            send_telegram_message("3. Бот не активирован, активирую..")
            return False
    except Exception as e:
        send_telegram_message(f"Ошибка при проверке GitHub Actions: {e}")
        return False

def update_and_restart_bot():
    # Команды для обновления и перезапуска bot.py
    try:
        send_telegram_message("7. Проверяю всё")
        # Здесь можно использовать команды для обновления кода, например git pull и запуск bot.py
        # Например:
        # os.system('git pull')
        # os.system('python bot.py &')
        send_telegram_message("Бот перезапущен.")
    except Exception as e:
        send_telegram_message(f"Ошибка при обновлении и перезапуске bot.py: {e}")

def main():
    while True:
        send_telegram_message("6. Задержка в 30 минут запущена")
        if check_workflows():
            send_telegram_message("Новая проверка через 30 минут.")
            time.sleep(CHECK_INTERVAL)
        else:
            send_telegram_message("4. Бот не активировался, пробую повторно...")
            update_and_restart_bot()
            send_telegram_message("5. Промежуток 2 минуты запущен")
            time.sleep(RETRY_INTERVAL)
            if check_workflows():
                send_telegram_message("Бот успешно активировался.")
                time.sleep(CHECK_INTERVAL)
            else:
                send_telegram_message("Бот не активировался после повторной попытки.")

if __name__ == '__main__':
    main()