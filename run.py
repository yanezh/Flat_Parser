from config import Config
from parsers.onliner import OnlinerParser
from flat_storage import FlatsManager
from telegram_bot import TelegramBot
import time


telegram_bot = TelegramBot(Config.TELEGRAM_BOT_TOKEN, Config.TELEGRAM_CHAT_ID)
flats_manager = FlatsManager(Config.STORE_FILE, telegram_bot)


while True:
    print("Updating")
    flats_found = []
    for url in Config.PARSED_URLS:
        try:
            flats = OnlinerParser.parse(url)
            flats_found.extend(flats)
        except Exception as e:
            telegram_bot.send_message("Произошла ошибка" + str(e))
    flats_manager.update(flats_found)
    time.sleep(Config.UPDATING_DELAY)
