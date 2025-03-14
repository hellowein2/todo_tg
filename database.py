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
            CREATE TABLE IF NOT EXISTS Tasks{user_id} (
            task TEXT NOT NULL,
            time TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
            )
            ''')

    def create_tak(self, user_id, task, time):
        with sqlite3.connect('ignore/data.db') as connection:
            cursor = connection.cursor()

            cursor.execute(f'INSERT INTO Tasks{user_id} (task, time) VALUES (?, ?)',
                           (task, time))

    def get_tasks(self, user_id):
        with sqlite3.connect('ignore/data.db') as connection:
            cursor = connection.cursor()

            pending_tasks = cursor.execute(f'SELECT rowid, * FROM Tasks{user_id} WHERE done = ?',
                                           (0,)).fetchall()
            completed_tasks = cursor.execute(f'SELECT rowid, * FROM Tasks{user_id} WHERE done = ?',
                                             (1,)).fetchall()

            return pending_tasks, completed_tasks

    def get_selected_task(self, user_id, task_id):
        with sqlite3.connect('ignore/data.db') as connection:
            cursor = connection.cursor()
            cursor.execute(f'SELECT * FROM Tasks{user_id} WHERE rowid = ?', (task_id,))
            task = cursor.fetchone()
            return task

    def delete_task(self, user_id, task_id):
        with sqlite3.connect('ignore/data.db') as connection:
            cursor = connection.cursor()
            cursor.execute(f'DELETE FROM Tasks{user_id} WHERE rowid = ?', (task_id,))

    def done_task(self, user_id, task_id):
        with sqlite3.connect('ignore/data.db') as connection:
            cursor = connection.cursor()
            cursor.execute(f'UPDATE Tasks{user_id} SET done = ? WHERE rowid = ?', (1, task_id))
            cursor.execute(f'UPDATE Tasks{user_id} SET time = ? WHERE rowid = ?',
                           (datetime.today().strftime("%d.%m.%Y %H:%M"), task_id))
