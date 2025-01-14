import telebot
import sqlite3
from datetime import datetime
from telebot import types
from ignore.api import API

API_TOKEN = API

__version__ = 'v.0.3'

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
        cursor.execute('INSERT OR REPLACE INTO Users (user_id, username) VALUES (?, ?)'
                       , (user_id, username))

        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS Tasks{user_id} (
        task TEXT NOT NULL,
        time TEXT NOT NULL
        )
        ''')


def add_task(message, edit_msg):
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Добавить задачу', callback_data='add_task')
    btn2 = types.InlineKeyboardButton(text='Просмотреть задачи', callback_data='view_tasks')
    kb.add(btn1, btn2)

    with sqlite3.connect('ignore/data.db') as connection:
        cursor = connection.cursor()

        cursor.execute(f'INSERT INTO Tasks{message.from_user.id} (task, time) VALUES (?, ?)',
                       (f'{message.text}', f'{datetime.today().strftime("%d.%m.%Y %H:%M")}'))

    bot.edit_message_text(chat_id=message.from_user.id, text=f'вы добавили задачу: {message.text}',
                          message_id=edit_msg.message_id,
                          reply_markup=kb)
    bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Добавить задачу', callback_data='add_task')
    btn2 = types.InlineKeyboardButton(text='Просмотреть задачи', callback_data='view_tasks')
    kb.add(btn1)
    kb.add(btn2)

    bot.send_message(message.chat.id, f'Ку {message.from_user.first_name} я todo list {__version__}', reply_markup=kb)

    add_users(message)


@bot.callback_query_handler(func=lambda call: call.data == 'back')
def back_to_main(call):
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Добавить задачу', callback_data='add_task')
    btn2 = types.InlineKeyboardButton(text='Просмотреть задачи', callback_data='view_tasks')
    kb.add(btn1, btn2)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f'todo list {__version__}', reply_markup=kb)


@bot.message_handler(content_types=['text'])
def del_message(message):
    bot.delete_message(message.chat.id, message.message_id)


@bot.callback_query_handler(func=lambda call: call.data == 'add_task')
def view_specific_task(call):
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Назад', callback_data='back')
    kb.add(btn1)
    edit_msg = bot.edit_message_text(chat_id=call.message.chat.id,
                                     message_id=call.message.message_id,
                                     text='Введите задачу:', reply_markup=kb)

    bot.register_next_step_handler(edit_msg, add_task, edit_msg)


@bot.callback_query_handler(func=lambda call: call.data == 'view_tasks')
def view_tasks(call):
    with sqlite3.connect('ignore/data.db') as connection:
        cursor = connection.cursor()
        kb = types.InlineKeyboardMarkup()
        count = []
        for i in cursor.execute(f'SELECT * FROM Tasks{call.message.chat.id}'):
            btn = types.InlineKeyboardButton(text=i[0], callback_data=i[1])
            count.append(btn)
        kb.add(*count)

        btn = types.InlineKeyboardButton('Назад', callback_data='back')
        kb.add(btn)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Ваши задачу:', reply_markup=kb)


if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)
