import telebot
import sqlite3
from telebot import types
from ignore.api import API

API_TOKEN = API

__version__ = 'v.0.1'

bot = telebot.TeleBot(API_TOKEN)


def add_users(message):
    user_id = message.from_user.id
    username = message.from_user.username

    with sqlite3.connect('ignore/data.db') as connection:
        cursor = connection.cursor()

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS Users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT
                )
            ''')
        cursor.execute('INSERT OR REPLACE INTO Users (user_id, username) VALUES (?, ?)', (user_id, username))


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Добавить задачу', callback_data=f'add_task')
    btn2 = types.InlineKeyboardButton(text='Просмотреть задачи', callback_data='view_tasks')
    kb.add(btn1, btn2)

    bot.send_message(message.chat.id, f'Ку {message.from_user.first_name} я todo list {__version__}', reply_markup=kb)

    add_users(message)


@bot.message_handler(content_types=['text'])
def chatting(message):
    bot.delete_message(message.chat.id, message.message_id)


bot.infinity_polling()
