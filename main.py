import telebot
import sqlite3
from telebot import types
from datetime import datetime
from ignore.api import API

API_TOKEN = API

__version__ = 'v.0.1'

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'Ку {message.from_user.first_name} я todo list {__version__}')


bot.infinity_polling()
