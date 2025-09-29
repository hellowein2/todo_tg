import telebot

from app.main_web import API_TOKEN


bot = telebot.TeleBot(API_TOKEN)



@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, 'kukich')


if __name__ == '__main__':
    bot.infinity_polling()