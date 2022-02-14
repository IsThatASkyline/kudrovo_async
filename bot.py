import telebot
import json
import time
from telebot import types
from config import token

bot = telebot.TeleBot(token)
                      
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Показать квартиры")
    markup.add(item1)
    bot.send_message(message.chat.id,'Привет', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def show_data(message):
    from pymongo import MongoClient
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://artklk12:artklk12@cluster0.ch7cl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial

    db = client["user_shopping_list"]
    list = db.user_1_items.find()

    for index, item in enumerate(list):
        if "Нет названия" in item['Название']:
            continue
        else:
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
bot.polling()
