import telebot
from datetime import datetime, timedelta
from telebot import types
import locale
from babel.dates import format_date
import os
import threading
from database import Database
import time
import re

db = Database('ignore/data.db')

API_TOKEN = os.environ.get('BOT_TOKEN')

__version__ = 'v.0.9.1'
bot = telebot.TeleBot(API_TOKEN)
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')


def validate_time_format(time_input):
    time_pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d$"
    if re.match(time_pattern, time_input):
        return True
    else:
        return False


def main_btn():
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Добавить задачу', callback_data='add_task')
    btn2 = types.InlineKeyboardButton(text='Просмотреть задачи', callback_data='view_tasks')
    kb.add(btn1, btn2)
    return kb


def add_task(message, edit_msg):
    kb = main_btn()
    bot.delete_message(message.chat.id, message.message_id)
    bot.edit_message_text(chat_id=message.from_user.id, text=f'Вы добавили задачу: {message.text}',
                          message_id=edit_msg.message_id,
                          reply_markup=kb)

    db.create_task(message.from_user.id, message.text, datetime.today().strftime("%d.%m.%Y %H:%M"))


def format_date_russian(date_string):
    date_object = datetime.strptime(date_string, "%d.%m.%Y %H:%M")
    return format_date(date_object, 'd MMMM', locale='ru')


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    kb = main_btn()

    bot.send_message(message.chat.id, f'Ку {message.from_user.first_name} я todo list {__version__}', reply_markup=kb)

    db.add_user(message.chat.id, message.from_user.first_name)


@bot.callback_query_handler(func=lambda call: call.data == 'back')
def back_to_main(call):
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    kb = main_btn()

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f'todo list {__version__}', reply_markup=kb)


@bot.message_handler(content_types=['text'])
def del_message(message):
    bot.delete_message(message.chat.id, message.message_id)


@bot.callback_query_handler(func=lambda call: call.data == 'add_task')
def pre_add_task(call):
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Назад', callback_data='back')
    kb.add(btn1)
    edit_msg = bot.edit_message_text(chat_id=call.message.chat.id,
                                     message_id=call.message.message_id,
                                     text='Введите задачу', reply_markup=kb)

    bot.register_next_step_handler(edit_msg, add_task, edit_msg)


@bot.callback_query_handler(func=lambda call: call.data == 'view_tasks')
def view_tasks(call):
    user_id = call.message.chat.id
    pending_tasks, completed_tasks = db.get_tasks(user_id)

    kb = types.InlineKeyboardMarkup()

    if pending_tasks or completed_tasks:
        for i in pending_tasks:
            btn = types.InlineKeyboardButton(text=i[1], callback_data=f'task_id_{i[0]}')
            kb.add(btn)
        if completed_tasks:
            for i in completed_tasks:
                btn = types.InlineKeyboardButton(text=f'{i[1]} ✅', callback_data=f'task_id_{i[0]}')
                kb.add(btn)

        btn = types.InlineKeyboardButton('Назад', callback_data='back')
        kb.add(btn)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Ваши задачи:', reply_markup=kb)
    else:
        btn = types.InlineKeyboardButton(text='Добавить задачу', callback_data='add_task')
        kb.add(btn)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Задач ещё нет', reply_markup=kb)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    task_id = call.data.split('_')[2]

    if call.data.startswith('task_id_'):
        handle_selected_task(call, task_id)
    elif call.data.startswith('delete_task_'):
        db.delete_task(call.message.chat.id, task_id)
        view_tasks(call)
    elif call.data.startswith('done_task_'):
        db.done_task(call.message.chat.id, task_id)
        view_tasks(call)

    elif call.data.startswith('remind_task_'):
        pre_remind_message(call, task_id)

    elif call.data == 'back':
        back_to_main(call)


def pre_remind_message(call, task_id):
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Назад', callback_data='back')
    kb.add(btn1)
    edit_msg = bot.edit_message_text(chat_id=call.message.chat.id,
                                     message_id=call.message.message_id,
                                     text='Введите в какое время напомнить:', reply_markup=kb)

    bot.register_next_step_handler(edit_msg, remind_message, edit_msg, task_id)


def remind_message(message, edit_msg, task_id):
    if validate_time_format(message.text):
        bot.delete_message(message.chat.id, message.message_id)
        kb = main_btn()
        bot.edit_message_text(chat_id=message.chat.id, message_id=edit_msg.message_id, text=f'Напомню в {message.text}',
                              reply_markup=kb)

        now = datetime.now()
        add_time = now + timedelta(minutes=1)

        db.remind_task(message.chat.id, task_id, add_time.strftime("%Y-%m-%d %H:%M"))
    else:
        bot.delete_message(message.chat.id, message.message_id)

        kb = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Назад', callback_data='back')
        kb.add(btn1)
        edit_msg = bot.edit_message_text(chat_id=message.chat.id, message_id=edit_msg.message_id,
                                         text=f'{message.text}'
                                              f' - некорректный формат времени. Введите время в формате HH:MM',
                                         reply_markup=kb)
        bot.register_next_step_handler(edit_msg, remind_message, edit_msg, task_id)


def handle_selected_task(call, task_id):
    task = db.get_selected_task(call.message.chat.id, task_id)

    formatted_date = format_date_russian(task[1])

    kb = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton('Назад', callback_data='view_tasks')

    if task[2] == 0:
        btn1 = types.InlineKeyboardButton('Вычеркнуть', callback_data=f'done_task_{task_id}')
        btn2 = types.InlineKeyboardButton('Удалить', callback_data=f'delete_task_{task_id}')
        btn3 = types.InlineKeyboardButton('Напомнить', callback_data=f'remind_task_{task_id}')
        kb.add(btn1, btn2)
        kb.add(btn3, btn_back)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=f'{task[0]} - созданно {formatted_date}', reply_markup=kb)
    else:
        btn = types.InlineKeyboardButton('Удалить', callback_data=f'delete_task_{task_id}')
        kb.add(btn)
        kb.add(btn_back)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=f'{task[0]} - сделанно {formatted_date}', reply_markup=kb)


def check_reminders():
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        tasks = db.get_reminded_tasks()
        for task in tasks:
            if task[4] == now:
                kb = main_btn()
                bot.send_message(task[5], f"Напоминание о задаче: {task[1]}", reply_markup=kb)
        time.sleep(60)


def start_reminder_service():
    reminder_thread = threading.Thread(target=check_reminders)
    reminder_thread.start()


if __name__ == '__main__':
    start_reminder_service()
    bot.infinity_polling(skip_pending=True)
