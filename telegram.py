import telebot
from config import *

bot=telebot.TeleBot(TELEGRAM_TOKEN)


def send_message(msg):
    pass
    bot.send_message(CID_CANAL_TESTS,msg,parse_mode="html")


if __name__ == "__main__":
    send_message("telegram")