import telebot

from config import keys
from extensions import APIException, Converter

from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message):
    text = "Этот бот умеет показывать стоимость некоторого количества одной валюты, выраженной в другой валюте.\n" \
           "Введите /help для просмотра синтаксиса ввода, /values для просмотра списка поддерживаемых валют."
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = "Синтаксис работы с ботом:\n\n" \
        "Первое слово: валюта, которую мы конвертируем;\n" \
           "Второе слово: валюта, в которую мы конвертируем;\n" \
           "В конце идёт количество конвертируемой валюты. Все вводимые данные разделяются пробелами.\n" \
           "Если коротко: Валюта1 Валюта2 Количество\n\n" \
           "/values: список всех доступных валют"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key.capitalize()))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        msg_input = message.text.split(' ')
        if len(msg_input) != 3:
            raise APIException("Неправильное количество параметров.\n"
                               "Введите обе валюты и количество первой валюты, разделённые пробелами.\n"
                               "Вы также можете воспользоваться командой /help для проверки синтаксиса.")

        quote, base, amount = msg_input
        total = Converter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        quote = quote.lower()
        base = base.lower()
        amount = amount.replace(",", ".")
        amount = float(amount)

        if amount % 1:
            quote = keys[quote]["gen_sing"]
        else:
            amount = int(amount)
            if amount % 10 == 1 and amount % 100 != 11:
                quote = keys[quote]["gen_sing"]
            else:
                quote = keys[quote]["gen_plural"]

        base = keys[base]["prep_plural"]
        text = f'Стоимость {amount} {quote} в {base} — {total}'
        bot.send_message(message.chat.id, text)


bot.polling()
