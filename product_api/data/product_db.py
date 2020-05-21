from __future__ import annotations

import sqlite3
from sqlite3 import Error
from threading import Lock, Thread
from typing import Optional


class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """

    _instance: Optional[ProductDb] = None

    _lock: Lock = Lock()
    """
    We now have a lock object that will be used to synchronize threads during
    first access to the Singleton.
    """

    def __call__(cls, *args, **kwargs):
        # Now, imagine that the program has just been launched. Since there's no
        # Singleton instance yet, multiple threads can simultaneously pass the
        # previous conditional and reach this point almost at the same time. The
        # first of them will acquire lock and will proceed further, while the
        # rest will wait here.
        with cls._lock:
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the Singleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the Singleton field
            # is already initialized, the thread won't create a new object.
            if not cls._instance:
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class ProductDb(metaclass=SingletonMeta):
    def __init__(self):
        try:
            self.con = sqlite3.connect(':memory:', check_same_thread=False)
            self.con.row_factory = self.__dict_factory

            print('Database created in-memory')

            self.__create_sqlite_tables()

            self.__seed_db()

        except Error:
            print(Error)

    def __create_sqlite_tables(self):
        cursor_obj = self.con.cursor()

        try:
            cursor_obj.execute(
                'CREATE TABLE products (id integer PRIMARY KEY, name text, price real , items_in_stock integer , items_reserved integer)')

            self.con.commit()

            print('Table created')

        except sqlite3.Error as e:
            print('Table creation exception. {}'.format(e))

    def __seed_db(self):
        cursor_obj = self.con.cursor()

        try:
            insert_query = 'INSERT INTO products (name, price, items_in_stock, items_reserved) VALUES (?, ?, ?, ?)'

            values = ('Coke', 5, 20, 0,)
            cursor_obj.execute(insert_query, values)

            values = ('Faxe kondi', 10, 17, 0,)
            cursor_obj.execute(insert_query, values)

            values = ('Fanta', 7, 11, 0,)
            cursor_obj.execute(insert_query, values)

            print('Db seeded')

        except sqlite3.Error as e:
            print('Insert exception. {}'.format(e))

    # For returning dictionaries rather than simply the values of the row
    def __dict_factory(self, cursor, row):
        d = {}

        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]

        return d

    def get_all(self):
        cursor_obj = self.con.cursor()

        try:
            query = 'SELECT * FROM products'
            cursor_obj.execute(query)

            query_result = cursor_obj.fetchall()

            return query_result

        except sqlite3.Error as e:
            print('Select exception. {}'.format(e))

    def get_by_id(self, product_id):
        cursor_obj = self.con.cursor()

        try:
            query = 'SELECT * FROM products WHERE id = ?'
            value = (product_id,)
            cursor_obj.execute(query, value, )

            query_result = cursor_obj.fetchall()

            return query_result

        except sqlite3.Error as e:
            print('Select exception. {}'.format(e))

    def update(self, name, price, items_in_stock, items_reserved, id):
        cursor_obj = self.con.cursor()

        try:
            query = 'UPDATE products SET name = ?, price = ?, items_in_stock = ?, items_reserved = ? WHERE id = ?'
            values = (name, price, items_in_stock, items_reserved, id,)
            cursor_obj.execute(query, values)

            return "Product was updated"

        except sqlite3.Error as e:
            print('Update exception. {}'.format(e))

    def insert(self, name, price, items_in_stock, items_reserved):
        cursor_obj = self.con.cursor()

        try:
            insert_query = 'INSERT INTO products (name, price, items_in_stock, items_reserved) VALUES (?, ?, ?, ?)'
            values = (name, price, items_in_stock, items_reserved,)
            cursor_obj.execute(insert_query, values)

            return "Product was created"

        except sqlite3.Error as e:
            print('Insert exception. {}'.format(e))

    def delete(self, product_id):
        cursor_obj = self.con.cursor()

        try:
            query = 'DELETE FROM products WHERE id = ?'
            values = (product_id,)
            cursor_obj.execute(query, values)

            return "Product was deleted"

        except sqlite3.Error as e:
            print('Delete exception. {}'.format(e))
