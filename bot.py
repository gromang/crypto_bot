import logging
import requests
import os

from dotenv import load_dotenv
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from boards import *

load_dotenv()
now = datetime.now()
logging.basicConfig(filename=f"{os.getcwd()}\{now.strftime('%Y-%m-%d__%H')}.log", level=logging.INFO,
                    filemode="a", format='%(levelname)s %(asctime)s : %(message)s')
logging.info(f'-------------------{now}-------------------')

PROXY = {
    "proxy_url": "socks5://t1.learn.python.ru:1080",
    "urllib3_proxy_kwargs": {"username": "learn", "password": "python"},
}


def main():

    updater = Updater(os.getenv("TOKEN"),
                      request_kwargs=PROXY,
                      use_context=True,
                      )

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler("help", help))
    updater.dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()


def start(update, context):
    update.message.reply_text(
        keyboard["Start"]["text"], parse_mode=ParseMode.MARKDOWN, reply_markup=get_keyboard(keyboard["Start"]["board_view"]))
    # Занесем в user_data словарь с вариантами следующей клавиатуры.
    # Чтобы не прописывать ветвления переходов по кнопкам,
    # в файле boards.py для каждой inlinekeyboard прописаны
    # соответсвия между кнопками и тем, куда они ведут
    context.user_data["routes"] = keyboard["Start"]["go_to"]
    # Создаем состояние, чтобы в функции button можно было понять, какая была предыдущая клавиатура
    context.user_data["came from"] = 'Start'
    # Создаем словарь параметров, которые будут заполнятся в зависимости от нажатий клавиатуры
    # и использоваться при формировании запросов
    context.user_data["params"] = {}


def get_keyboard(inline_table):
    # Функция генерации клавиатуры, принимает вложенный список
    # с названиями кнопок клавиатуры и возвращает такой же по структуре
    # вложенный список из функций кнопок InlineKeyboardButton.
    # Сделал, с целью не плодить множество описаний функций клавиатур
    # И упростить само описание инлайн-клавиатур, переведя его в вид словаря в файле boards.py
    keyboard = []

    for i, l in enumerate(inline_table):
        keyboard.append([])
        for v in l:
            keyboard[i].append(InlineKeyboardButton(v, callback_data=v))

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def button(update, context):
    # Забираем из callback_data данные нажатия
    query = update.callback_query
    data = query.data
    # Определяем, какая клавиатура из ограниченного списка путей
    # соответсвует преданному значению нажатия
    name = context.user_data["routes"].get(data)
    # Забираем название предыдущей клавиатуры
    last_page = context.user_data["came from"]
    # Создаем переменную текста, которую отобразим на новой клавиатуре
    text = ''
    # Здесь смысл в том, чтобы определить -надо записывать в параметры что-то, или нет
    # Для этого используем маркер action прописанный для каждой клавиатуры в ее параметрах
    if keyboard[last_page]['action'] == 'store':
        context.user_data["params"].update({last_page: data})

    if keyboard[name]['action'] == "get chart":
        pair = context.user_data["params"]["Chart_pair"]
        interval = context.user_data["params"]["Interval"]
        url = f"http://localhost:5000/plotly?pair={pair}&interval={interval}"
        text = f"График {pair} {interval} {url}"

    # if keyboard[last_page]['action'] == "send order":
    #     pair = context.user_data["params"]["Trade_pair"]
    #     exch = context.user_data["params"]["Exchange"]

    #     get_lots(update, context)
    #     lots = context.user_data["params"]["lots"]

    #     try:

    #     print(f'{pair} и {exch} -- {lots}')
    #         text = f'Отправлен приказ на биржу {exch} на покупку {pair} в размере {lots}'
    #     except (ValueError, TypeError):
    #         text = "Напишите кол-во лотов"

    if name in keyboard:
        query.edit_message_text(text=text or keyboard[name]["text"],
                                reply_markup=get_keyboard(keyboard[name]["board_view"]))
        context.user_data["routes"] = keyboard[name]["go_to"]

    context.user_data["came from"] = name


# def get_lots(update, context):
#     lots = update.message.text
#     lots = float(lots)
#     context.user_data["params"].update({"lots": lots})


def help(update, context):
    update.message.reply_text("Use /start to test this bot.")


def error(update, context):
    """Log Errors caused by Updates."""
    logging.info('Update "%s" caused error "%s"', update, context.error)


if __name__ == "__main__":
    main()
