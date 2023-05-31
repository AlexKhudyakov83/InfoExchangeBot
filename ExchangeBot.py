import telebot
from telebot import types
from extensions import ConvertionException, CryptoConverter
from currency import keys, TOKEN

bot = telebot.TeleBot(TOKEN)


# Стартовый обработчик. Создаем в нем две кнопки
@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    text = f"Здравствуйте, {message.from_user.full_name}, для начала работы введите:\n" \
           f" 'наименование валюты' 'в какую валюту переводим' 'количество переводимой валюты'\n" \
           f"👇Для удобства есть две кнопки👇"
    button1 = types.KeyboardButton("/❓help❓")
    button2 = types.KeyboardButton("/💱values")
    markup.add(button1, button2)
    bot.reply_to(message, text, reply_markup=markup)


# Обработчик кнопки валюта. В нем справочные кнопки по каждой валюте
@bot.message_handler(commands=["💱values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key, ))
    text += "\nСправка о каждой, если интересно:"
    button_values = types.InlineKeyboardMarkup()
    button_usd = types.InlineKeyboardButton("доллар", url='https://ru.wikipedia.org/wiki/Доллар_США')
    button_eur = types.InlineKeyboardButton("евро", url='https://ru.wikipedia.org/wiki/Евро')
    button_rub = types.InlineKeyboardButton("рубль", url='https://ru.wikipedia.org/wiki/Российский_рубль')
    button_jpy = types.InlineKeyboardButton("йена", url='https://ru.wikipedia.org/wiki/Иена')
    button_gbp = types.InlineKeyboardButton("фунт", url='https://ru.wikipedia.org/wiki/Фунт_стерлингов')
    button_btc = types.InlineKeyboardButton("биткоин", url='https://ru.wikipedia.org/wiki/Биткойн')
    button_values.add(button_usd, button_eur, button_rub, button_jpy, button_gbp, button_btc)
    bot.send_message(message.chat.id, text.format(message.from_user), reply_markup=button_values)


# Обработчик кнопки помощь
@bot.message_handler(commands=["❓help❓"])
def button_help(message):
    bot.send_message(message.chat.id, f"{message.from_user.full_name}, необходимо вводить:\n"
                                      f"'наименование валюты' 'в какую валюту переводим' и 'количество "
                                      f"переводимой валюты'")


# Главный обработчик
@bot.message_handler(content_types=["text"])
def converter(message: telebot.types.Message):
    try:
        values = message.text.split(" ")
        if len(values) != 3:
            raise ConvertionException('Не правильное количество параметров')
        quote, base, amount = values
        total_base = CryptoConverter.convert(str.lower(quote), str.lower(base), amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Команда мне не понятна\n{e}")
    else:
        text = f'Цена {amount} {quote} в {base} равна {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
