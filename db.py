import sqlite3
import log
from config import db_name


class DB:
    __instance = None
    connection = None
    cursor = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __del__(self):
        DB.__instance = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(db_name)
            self.cursor = self.connection.cursor()

        except sqlite3.Error as error:
            log.error("Ошибка при подключении к sqlite", error)

    def close(self):
        if self.connection and isinstance(self.connection, sqlite3.Connection):
            self.connection.close()

    def ini_tables(self):
        self.connect()
        self.connection.execute('''CREATE TABLE IF NOT EXISTS timers
                             (ID INTEGER PRIMARY KEY    AUTOINCREMENT,
                             chat           INT    NOT NULL,
                             timerstatus            INT     NOT NULL);''')
        self.connection.commit()
        self.close()

    def insert_timer(self, data):
        chat = data['chat']
        timerstatus = data['timerstatus']

        self.connect()
        res = self.connection.execute(f'SELECT * FROM timers WHERE chat="{chat}"').fetchall()

        if not len(res):
            sql = f'INSERT INTO timers (chat, timerstatus) VALUES({chat}, {timerstatus})'
            self.cursor.execute(sql)
            self.connection.commit()
            print('insert lastrowid', self.cursor.lastrowid)

        else:
            sql = f'UPDATE timers SET timerstatus={timerstatus} WHERE chat={chat}'
            self.cursor.execute(sql)
            self.connection.commit()
            print('update lastrowid', self.cursor.lastrowid)

    def start_timer(self, chat):
        self.insert_timer({'chat': chat, 'timerstatus': 1})

    def stop_timer(self, chat):
        self.insert_timer({'chat': chat, 'timerstatus': 0})

    def is_timer_in_progress(self, chat):
        self.connect()
        timerstatus = self.connection.execute(f'SELECT timerstatus FROM timers WHERE chat={chat}').fetchone()
        return timerstatus[0]

    def insert(self, table, fields):
        self.connect()
        self.connection.execute("")
        print(f'fields: {fields}')

    def get_all_active_subscriptions(self):
        self.connect()
        self.cursor.execute("SELECT chat FROM timers WHERE timerstatus=1")
        return self.cursor.fetchall()
