import telebot
from system import *
from trade import *
from config import *
import threading #pq no s'aturi el fil del programa principal


enbitbot=telebot.TeleBot(TELEGRAM_ENBITBOT)

@enbitbot.message_handler(commands=['percent'])
def cmp_percent(message):
    msg="<b>PERCENT:</b>"+"\n"
    info=calculate_trade("INC","PLSX",True)
    msg+=info+"\n"
    info=calculate_trade("pDAI","PLSX",True)
    msg+=info+"\n"
    enbitbot.reply_to(message,msg,parse_mode="html")

@enbitbot.message_handler(commands=['setmax'])
def cmp_setmax(message):
    dades=message.text.split(" ")
    print(dades)
    set_max_percent2(float(dades[2]),dades[1])

def recive_msgs():
    enbitbot.infinity_polling()


if __name__ == "__main__":
    enbitbot.set_my_commands([
        telebot.types.BotCommand("/percent","percent"),
        telebot.types.BotCommand("/setmax","set maxim"),

    ])
    hilo_bot=threading.Thread(name="hilo_bot",target=recive_msgs)
    hilo_bot.start()
    print("bot iniciat")