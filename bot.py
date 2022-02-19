import telebot
import time
from telebot import types
from config import token

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Показать квартиры")
    markup.add(item1)
    bot.send_message(message.chat.id, 'Привет', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def filter_menu(message):
    filt = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("По цене")
    item2 = types.KeyboardButton("По кол-ву комнат")
    filt.add(item1, item2)
    mesg = bot.send_message(message.chat.id, f'Выберите фильтр', reply_markup=filt)
    bot.register_next_step_handler(mesg, subfilter_menu)

def subfilter_menu(message):
    filter = message.text

    if filter == "По цене":
        sub = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("<=20к")
        item2 = types.KeyboardButton("20к-30к")
        item3 = types.KeyboardButton(">=30к")
        sub.add(item1, item2, item3)
        mesg = bot.send_message(message.chat.id, f'Выберите ценовой диапазон', reply_markup=sub)
        bot.register_next_step_handler(mesg, show_data)
    elif filter == "По кол-ву комнат":
        sub = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("1-комнатные")
        item2 = types.KeyboardButton("2-комнатные")
        sub.add(item1, item2)
        mesg = bot.send_message(message.chat.id, f'Выберите кол-во комнат', reply_markup=sub)
        bot.register_next_step_handler(mesg, show_data)
    else:
        bot.send_message(message.chat.id, 'Используйте клавиатуру')


def show_data(message):

    filt = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("По цене")
    item2 = types.KeyboardButton("По кол-ву комнат")
    filt.add(item1, item2)

    subcat = message.text

    from pymongo import MongoClient
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://artklk12:artklk12@cluster0.ch7cl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial

    db = client["user_shopping_list"]
    list = db.user_1_items.find()

    if subcat == "<=20к":
        for index, item in enumerate(list):
            try:
                if int(item['Цена'].rsplit("₽")[0].replace(" ", "")) <= 20000:
                    try:
                        card = f"{item['Название']} \n" \
                               f"{item['Картинка']} \n" \
                               f"{item['Цена']}\n\n" \
                               f"{item['Адрес']} \n\n" \
                               f"{item['Описание']}\n" \
                               f"{item['Ссылка']}\n"
                        bot.send_message(message.chat.id, card)
                    except:
                        time.sleep(1)
            except ValueError:
                continue
        mesg = bot.send_message(message.chat.id, f'Выберите фильтр', reply_markup=filt)
        bot.register_next_step_handler(mesg, subfilter_menu)

    elif subcat == "20к-30к":
        for index, item in enumerate(list):
            try:
                if int(item['Цена'].rsplit("₽")[0].replace(" ","")) > 20000 and int(item['Цена'].rsplit("₽")[0].replace(" ","")) < 30000:
                    try:
                        card = f"{item['Название']} \n" \
                               f"{item['Картинка']} \n" \
                               f"{item['Цена']}\n\n" \
                               f"{item['Адрес']} \n\n" \
                               f"{item['Описание']}\n" \
                               f"{item['Ссылка']}\n"
                        bot.send_message(message.chat.id, card)
                    except:
                        time.sleep(1)
            except ValueError:
                continue
        mesg = bot.send_message(message.chat.id, f'Выберите фильтр', reply_markup=filt)
        bot.register_next_step_handler(mesg, subfilter_menu)


    elif subcat == ">=30к":
        for index, item in enumerate(list):
            try:
                if int(item['Цена'].rsplit("₽")[0].replace(" ","")) >= 30000:
                    try:
                        card = f"{item['Название']} \n" \
                               f"{item['Картинка']} \n" \
                               f"{item['Цена']}\n\n" \
                               f"{item['Адрес']} \n\n" \
                               f"{item['Описание']}\n" \
                               f"{item['Ссылка']}\n"
                        bot.send_message(message.chat.id, card)
                    except:
                        time.sleep(1)
            except ValueError:
                continue
        mesg = bot.send_message(message.chat.id, f'Выберите фильтр', reply_markup=filt)
        bot.register_next_step_handler(mesg, subfilter_menu)

    elif subcat == "1-комнатные":
        for index, item in enumerate(list):
            if "1-комн." in item["Название"]:
                try:
                    card = f"{item['Название']} \n" \
                           f"{item['Картинка']} \n" \
                           f"{item['Цена']}\n\n" \
                           f"{item['Адрес']} \n\n" \
                           f"{item['Описание']}\n" \
                           f"{item['Ссылка']}\n"
                    bot.send_message(message.chat.id, card)
                except:
                    time.sleep(1)
        mesg = bot.send_message(message.chat.id, f'Выберите фильтр', reply_markup=filt)
        bot.register_next_step_handler(mesg, subfilter_menu)

    elif subcat == "2-комнатные":
        for index, item in enumerate(list):
            if "2-комн." in item["Название"]:
                try:
                    card = f"{item['Название']} \n" \
                           f"{item['Картинка']} \n" \
                           f"{item['Цена']}\n\n" \
                           f"{item['Адрес']} \n\n" \
                           f"{item['Описание']}\n" \
                           f"{item['Ссылка']}\n"
                    bot.send_message(message.chat.id, card)
                except:
                    time.sleep(1)
        mesg = bot.send_message(message.chat.id, f'Выберите фильтр', reply_markup=filt)
        bot.register_next_step_handler(mesg, subfilter_menu)
    else:
        bot.send_message(message.chat.id, 'Используйте клавиатуру')


bot.polling()
