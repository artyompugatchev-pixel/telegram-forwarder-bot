import asyncio
import threading
from flask import Flask
from telethon import TelegramClient, events

# =========================================================
# ТВОИ ДАННЫЕ
# =========================================================

api_id = 39742480
api_hash = '62bbd4b780b3ca12d7bc9ae75276d88e'

# Создаём клиент от имени ТВОЕГО аккаунта (не бота)
client = TelegramClient('session_name', api_id, api_hash)

SOURCE_CHAT = '@baraholer'
DEST_CHAT = '@pugatchev999'

# =========================================================
# КОД ПЕРЕСЫЛЬЩИКА
# =========================================================

@client.on(events.NewMessage(chats=SOURCE_CHAT))
async def forward_message(event):
    try:
        await client.send_message(DEST_CHAT, event.message)
        print('✅ Переслано!')
    except Exception as e:
        print(f'❌ Ошибка: {e}')

# =========================================================
# ВЕБ-СЕРВЕР ДЛЯ RENDER
# =========================================================

flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return "Bot is running!"

def run_flask():
    flask_app.run(host='0.0.0.0', port=8080)

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    print('🚀 Бот-пересыльщик запущен!')
    client.start()
    client.run_until_disconnected()

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    run_flask()
