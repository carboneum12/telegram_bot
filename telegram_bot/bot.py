import telebot
from telebot.types import Message
from telebot import apihelper
from pymongo import MongoClient
from telegram_bot.google_parse import mistakes_correction


TOKEN = '919317108:AAGDdVDvdHj-xDvrBkjxqmSAjjmArFdSfgY'
#Работает либо с впн либо с Proxy
#apihelper.proxy = {'https':'https://128.106.14.225:10378'}

bot = telebot.TeleBot(TOKEN)
client = MongoClient('localhost', 27017)
db = client['message_history']


@bot.message_handler(commands=['start', 'help'])
def start(message: Message):
    bot.send_message(message.from_user.id, 'Привет, я помогу отличить кота от хлеба. Объект перед тобой квадратный?')


@bot.message_handler(content_types=['text'])
def echo_all(message: Message):
    print(message.text)
    #В бд мы будем создавать коллекции, названия которых совпадают с ником пользователя
    collection_name = message.from_user.username
    try:
        db.create_collection(collection_name) #Проверяем, есть ли уже такая коллекция
    except Exception: #Если есть, то просто добавляем документ
        col = db.get_collection(collection_name)
        col.insert_one({'user': collection_name,
                                   'text': message.text,
                                   'date': message.date})
    else:
        add_collection = db.create_collection(collection_name)
        add_collection.insert_one({'user': collection_name,
                                   'text': message.text,
                                   'date': message.date})

    mes = message.text.lower()  #Решаем проблему с регистром сообщений
    mess = mistakes_correction(mes) #Функция для частичного исправления ошибок. Просто парсит гугл со вставленным сообщением
    try:
        mess[0] #Проверяем, сделал ли поьзователь ошибку, если да, то mess вернет не пустой список
    except IndexError:
        if mes == 'ага' or mes == 'да' or mes == 'пожалуй':
            bot.send_message(message.from_user.id, 'Это хлеб!')
        elif mes == 'нет' or mes == 'ноуп' or mes == 'найн':
            bot.send_message(message.from_user.id, 'У него есть уши?')
            bot.register_next_step_handler(message, ear)
        else:
            bot.send_message(message.from_user.id, f'Ты написал "{mes}", но я тебя не понял. Я лишь отличаю хлеб от кота :) Напиши /start')
    else:
        response = ' '.join(mess)
        if response == 'ага' or response == 'да' or response == 'пожалуй':
            bot.send_message(message.from_user.id, 'Да? Значит это хлеб!')
        elif response == 'нет' or response == 'ноуп' or response == 'найн':
            bot.send_message(message.from_user.id, 'Нет? А у него есть уши?')
            bot.register_next_step_handler(message, ear)
        else:
            bot.send_message(message.from_user.id, f'Похоже у тебя лапки вместо рук, может ты и хотел сказать "{response}", но я лишь отличаю хлеб от кота! Пиши /start')


@bot.message_handler(content_types=['text'])
def ear(message):
    print(message.text)
    collection_name = message.from_user.username
    try:
        db.create_collection(collection_name)
    except Exception:
        col = db.get_collection(collection_name)
        col.insert_one({'user': collection_name,
                                   'text': message.text,
                                   'date': message.date})
    else:
        add_collection = db.create_collection(collection_name)
        add_collection.insert_one({'user': collection_name,
                                   'text': message.text,
                                   'date': message.date})
    mes = message.text.lower()
    if mes == 'ага' or mes == 'да' or mes == 'пожалуй':
        bot.send_message(message.from_user.id, 'Это кот!')
    elif mes == 'нет' or mes == 'ноуп' or mes == 'найн':
        bot.send_message(message.from_user.id, 'Это хлеб!')
    elif message.text == '/start':
        return start(message)
    else:
        bot.send_message(message.from_user.id, 'Я тебя не понимаю, напиши /start')




bot.polling(none_stop=True, interval=0)
