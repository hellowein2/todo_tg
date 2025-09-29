import os
import telebot

API_TOKEN = os.environ.get("API_TOKEN")


bot = telebot.TeleBot(API_TOKEN)



@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, 'kukich')


if __name__ == '__main__':
    bot.infinity_polling()