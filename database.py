import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self._create_tables()

    def _create_tables(self):
        with sqlite3.connect('ignore/data.db') as connection:
            cursor = connection.cursor()

            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT
                    )
                ''')

    def add_user(self, user_id, username):
        with sqlite3.connect('ignore/data.db') as connection:
            cursor = connection.cursor()

            cursor.execute('INSERT OR REPLACE INTO Users (user_id, username) VALUES (?, ?)'
                           , (user_id, username))

            cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS Tasks (
            task TEXT NOT NULL,
            time TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0,
            reminder_time TEXT,
            user_id INTEGER NOT NULL
            )
            ''')

    def create_task(self, user_id, task, time):
        with sqlite3.connect('ignore/data.db') as connection:
            cursor = connection.cursor()

            cursor.execute(f'INSERT INTO Tasks (task, time, user_id) VALUES (?, ?, ?)',
                           (task, time, user_id))

    def get_tasks(self, user_id):
        with sqlite3.connect('ignore/data.db') as connection:
            cursor = connection.cursor()

            pending_tasks = cursor.execute(f'SELECT rowid, * FROM Tasks WHERE done = ? AND user_id = ?',
                                           (0, user_id)).fetchall()
            completed_tasks = cursor.execute(f'SELECT rowid, * FROM Tasks WHERE done = ? AND user_id = ?',
                                             (1, user_id)).fetchall()

            return pending_tasks, completed_tasks

    def get_reminded_tasks(self):
        with sqlite3.connect('ignore/data.db') as connection:
            cursor = connection.cursor()

            cursor.execute(f'SELECT rowid, * FROM Tasks WHERE reminder_time IS NOT NULL AND done = 0')
            tasks = cursor.fetchall()
            return tasks

    def get_selected_task(self, user_id, task_id):
        with sqlite3.connect('ignore/data.db') as connection:
            cursor = connection.cursor()
            cursor.execute(f'SELECT * FROM Tasks WHERE rowid = ? AND user_id = ?', (task_id, user_id))
            task = cursor.fetchone()
            return task

    def delete_task(self, user_id, task_id):
        with sqlite3.connect('ignore/data.db') as connection:
            cursor = connection.cursor()
            cursor.execute(f'DELETE FROM Tasks WHERE rowid = ? AND user_id = ?', (task_id, user_id))

    def done_task(self, user_id, task_id):
        with sqlite3.connect('ignore/data.db') as connection:
            cursor = connection.cursor()
            cursor.execute(f'UPDATE Tasks SET done = ? WHERE rowid = ? AND user_id = ?',
                           (1, task_id, user_id))
            cursor.execute(f'UPDATE Tasks SET time = ? WHERE rowid = ? AND user_id = ?',
                           (datetime.today().strftime("%d.%m.%Y %H:%M"), task_id, user_id))
            cursor.execute(f'UPDATE Tasks SET reminder_time = ? WHERE rowid = ?',
                           (None, task_id))

    def remind_task(self, user_id, task_id, time):
        with sqlite3.connect('ignore/data.db') as connection:
            cursor = connection.cursor()

            cursor.execute(f'UPDATE Tasks SET reminder_time = ? WHERE rowid = ? AND user_id = ?',
                           (time, task_id, user_id))

    def clear_remind(self, task_id, time):
        with sqlite3.connect('ignore/data.db') as connection:
            cursor = connection.cursor()

            cursor.execute(f'UPDATE Tasks SET reminder_time = ? WHERE rowid = ?',
                           (time, task_id))
