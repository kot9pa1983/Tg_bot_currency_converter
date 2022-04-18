import telebot
from  tokens_and_keys import *
from extensions import *

bot = telebot.TeleBot(TOKEN)

keys = {'Евро': 'EUR',
'Юань': 'CNY',
'Рубль': 'RUB',
'Доллар': 'USD',
'Биткоин': 'BTC',
'Эфир': 'ETH'}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if greet_count := 1:
        bot.send_message(message.chat.id, f"Для получения помощи введите команду: /help")
    else:
        bot.send_message(message.chat.id, f"Приветствую, {message.chat.username}")
        greet_count = 1
    
    

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты> <имя валюты, в которую надо перевести> <количество переводимой валюты>\n\n Просмотреть список доступных валют: команда /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        parameters = message.text.split(' ')
        
        if len(parameters) != 3:
            raise APIException('Неверное кол-во параметров')
        base, quote, amount = parameters
        total_base = CurrencyConverter(base, quote, amount)
        text = f'Цена {amount} {base} в {quote} -> {total_base.get_price(base, quote, amount)}'
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка пользователя\n {e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Не удалось обработать команду\n {e}')
    else:
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)