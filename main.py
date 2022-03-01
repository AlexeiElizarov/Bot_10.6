from extensions import *
from config import *

import telebot

api = 'http://api.exchangeratesapi.io/v1/latest?access_key=dc6be5790633985270dc0449a08ab3ba&symbols=USD,RUB,AUD,CAD,PLN,MXN&format=1'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def hadler_start_help(message):
    bot.send_message(message.chat.id, "Бот выводит цену запрашиваемой валюты. Цена выводится в указанной валюте.\n"
                                      "Введите: <имя валюты цену которой вы хотите узнать> <имя валюты в которой надо "
                                      "узнать цену первой валюты> <количество первой валюты>\n"
                                      "Доступные валюты - команда: /values")

@bot.message_handler(commands=['values'])
def handler_values(message):
    text = "Доступные валюты:"
    for key in currency_keys.keys():
        text = '\n'.join((text, key, ))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def handler_text(message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException('Должно быть 3 параметра')
        quote, base, amount = Currency.check_data(*values)
        conn = Currency()
        result = conn.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, e)
    except Exception as e:
        bot.reply_to(message, f'Не могу  обработать команду\n{e}')
    else:
        bot.send_message(message.chat.id, f"Цена {amount} {quote} в {base} - {result:.2f}")

bot.polling(none_stop=True)
