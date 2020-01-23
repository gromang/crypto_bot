import logging
import requests
import os

from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
)

from boards_config import boards
from settings import TOKEN, PROXY, intervals

now = datetime.now()
logging.basicConfig(
    filename=f"{os.getcwd()}\{now.strftime('%Y-%m-%d__%H')}.log",
    level=logging.INFO,
    filemode="a",
    format="%(levelname)s %(asctime)s : %(message)s",
)
logging.info(f"-------------------{now}-------------------")


def main():
    updater = Updater(TOKEN, request_kwargs=PROXY, use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler("help", help))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, get_lots))
    updater.dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()


def start(update, context):
    # 1. Сформируем стартовую клавиатуру.
    #    Для этого заберем необходимые параметры из boards_config.py
    # 2. Занесем в user_data словарь с вариантами следующей клавиатуры.
    #    Это необходимо, чтобы не прописывать ветвления переходов по кнопкам.
    #    Поэтому в файле boards_config.py для каждой inlinekeyboard прописаны
    #    соответсвия между кнопками и тем, куда они ведут.
    # 3. Создаем состояние, чтобы в функции button можно было понять,
    #    какая была предыдущая клавиатура
    # 4. Создаем словарь параметров, которые будут заполнятся
    #    в зависимости от нажатий клавиатуры
    #    и использоваться при формировании запросов
    text = boards["Start"]["text"]
    markup = get_keyboard(boards["Start"]["board_view"])
    update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)
    context.user_data["routes"] = boards["Start"]["go_to"]
    context.user_data["came from"] = "Start"
    context.user_data["params"] = {}


def get_keyboard(board_view):
    # Функция генерации клавиатуры, принимает вложенный список
    # с названиями кнопок клавиатуры и возвращает такой же по структуре
    # вложенный список из функций кнопок InlineKeyboardButton.
    # Сделал, с целью не плодить множество описаний функций клавиатур
    # И упростить само описание инлайн-клавиатур,
    # переведя его в вид словаря в файле boards_config.py
    markup = []

    for i, l in enumerate(board_view):
        markup.append([])
        for v in l:
            markup[i].append(InlineKeyboardButton(v, callback_data=v))

    reply_markup = InlineKeyboardMarkup(markup)
    return reply_markup


def button(update, context):
    # 1. Забираем из callback_data данные нажатия в переменную data
    # 2. Определяем имя вызванной клавиатуры. Для этого сопоставляем нажатую кнопку
    #    с прописанной для нее клавиатурой в словаре routes
    # 3. Забираем название предыдущей клавиатуры в last_page
    # 4. Создаем переменную текста, которую отобразим на новой клавиатуре
    # 5. Через маркер action определяем, нужно ли выполнить какое-либо действие для этой
    #    клавиатуры
    query = update.callback_query
    data = query.data
    this_page = context.user_data["routes"].get(data)
    last_page = context.user_data["came from"]
    text = ""
    parameters = context.user_data["params"]

    if boards[last_page]["action"] == "save":
        parameters.update({last_page: data})

    if boards[this_page]["action"] == "get_chart":
        text = get_chart(parameters)

    if boards[last_page]["action"] == "make_order":
        text = make_order(parameters)

    if boards[last_page]["action"] == "send_order":
        text = send_order(parameters)

    if this_page in boards:
        query.edit_message_text(
            text=text or boards[this_page]["text"],
            reply_markup=get_keyboard(boards[this_page]["board_view"]),
        )
        context.user_data["routes"] = boards[this_page]["go_to"]

    context.user_data["came from"] = this_page


def get_chart(parameters):
    pair = parameters["Chart_pair"]
    interval = intervals[parameters["Interval"]]
    url = f"http://localhost:5000/plotly?pair={pair}&interval={interval}"
    text = f"График {pair} {interval} {url}"
    return text


def make_order(parameters):
    # Сделать проверку на наличие лотов и что состоит только из цифр
    pair = parameters["Trade_pair"]
    exch = parameters["Exchange"]
    lots = parameters["lots"]
    direction = parameters["Buy_Sell"]
    text = f"Отправить приказ на биржу {exch} : {direction.upper()}  {lots}  {pair} ?"
    return text


def send_order(parameters):
    # Сделать проверку на наличие лотов и что состоит только из цифр
    pair = parameters["Trade_pair"]
    exch = parameters["Exchange"]
    lots = parameters["lots"]
    direction = parameters["Buy_Sell"]
    text = f"{exch} : {direction.upper()}  {lots}  {pair}"
    return text


def get_lots(update, context):
    lots = update.message.text
    lots = float(lots)
    context.user_data["params"].update({"lots": lots})


def help(update, context):
    update.message.reply_text("Use /start to test this bot.")


def error(update, context):
    """Log Errors caused by Updates."""
    logging.info('Update "%s" caused error "%s"', update, context.error)


if __name__ == "__main__":
    main()
