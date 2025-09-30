import os
import telebot

API_TOKEN = os.environ.get("BOT_TOKEN")


bot = telebot.TeleBot(API_TOKEN)



@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(chat_id=message.chat.id, text='wewewe')


if __name__ == '__main__':
    bot.infinity_polling()