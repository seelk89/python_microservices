from __future__ import annotations

import sqlite3
from datetime import date
from sqlite3 import Error
from threading import Lock
from typing import Optional


class SingletonMeta(type):
    '''
    This is a thread-safe implementation of Singleton.
    '''

    _instance: Optional[OrderDb] = None

    _lock: Lock = Lock()
    '''
    We now have a lock object that will be used to synchronize threads during
    first access to the Singleton.
    '''

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


class OrderDb(metaclass=SingletonMeta):
    def __init__(self):
        try:
            # There might be a better solution than check_same_thread=False
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
                'CREATE TABLE orders (id integer PRIMARY KEY, date text, customer_id integer, order_status text, order_lines integer)')

            self.con.commit()

            cursor_obj.execute(
                'CREATE TABLE order_lines (id integer PRIMARY KEY, order_id integer, product_id integer, quantity integer)')

            self.con.commit()

            print('Tables created')

        except sqlite3.Error as e:
            print('Table creation exception. {}'.format(e))

    def __seed_db(self):
        cursor_obj = self.con.cursor()
        today = date.today()

        try:
            insert_query = 'INSERT INTO orders (date, customer_id, order_lines) VALUES (?, ?, ?)'
            values = (today.strftime("%d/%m/%Y"), 1, 1,)
            cursor_obj.execute(insert_query, values)

            values = (today.strftime("%d/%m/%Y"), 2, 1,)
            cursor_obj.execute(insert_query, values)

            insert_query = 'INSERT INTO order_lines (order_id, product_id, quantity) VALUES (?, ?, ?)'
            values = (1, 1, 10,)
            cursor_obj.execute(insert_query, values)

            insert_query = 'INSERT INTO order_lines (order_id, product_id, quantity) VALUES (?, ?, ?)'
            values = (1, 2, 60,)
            cursor_obj.execute(insert_query, values)

            print('Database seeded')

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
            # Try to join order_lines to the order they belong to
            # query = 'SELECT * FROM orders JOIN order_lines ON order.order_lines = order_lines.order_id'
            query = 'SELECT * FROM orders'
            cursor_obj.execute(query)

            query_result = cursor_obj.fetchall()

            return query_result

        except sqlite3.Error as e:
            print('Select exception. {}'.format(e))

    def get_by_id(self, id):
        cursor_obj = self.con.cursor()
        try:
            query = "SELECT id, date, customer_id, order_status FROM orders WHERE orders.id = ?"
            # query = 'SELECT * FROM orders LEFT JOIN order_lines ON orders.id = order_lines.order_id WHERE orders.id = ?'
            # query = "SELECT *,((SELECT * FROM order_lines WHERE order_lines.order_id = orders.id) AS order_lines) AS order_lines FROM orders WHERE orders.id = ?"
            value = (id,)
            cursor_obj.execute(query, value, )
            query_result = cursor_obj.fetchall()

            order_id = query_result[0]["id"]
            query2 = "SELECT * FROM order_lines WHERE order_lines.order_id = ?"
            value2 = (order_id,)
            cursor_obj.execute(query2, value2, )
            order_lines_result = cursor_obj.fetchall()
            query_result[0]["order_lines"] = order_lines_result

            return query_result

        except sqlite3.Error as e:
            print('Select exception. {}'.format(e))

    def update(self, date, customer_id, order_status, id):
        cursor_obj = self.con.cursor()

        try:
            query = 'UPDATE orders SET date = ?, customer_id = ?, order_status = ? WHERE id = ?'
            values = (date, customer_id, order_status, id,)
            cursor_obj.execute(query, values)

            return 'Order was updated'

        except sqlite3.Error as e:
            print('Update exception. {}'.format(e))

    def insert(self, date, customer_id, order_status, order_lines):
        cursor_obj = self.con.cursor()

        try:
            query = 'INSERT INTO orders (date, customer_id, order_status) VALUES (?, ?, ?)'
            values = (date, customer_id, order_status,)
            cursor_obj.execute(query, values)
            new_order_id = cursor_obj.lastrowid

            for order_line in order_lines:
                query = 'INSERT INTO order_lines (order_id, product_id, quantity) VALUES (?, ?, ?)'
                values = (new_order_id, order_line["product_id"], order_line["quantity"],)
                cursor_obj.execute(query, values)

            return new_order_id

        except sqlite3.Error as e:
            print('Insert exception. {}'.format(e))

    def delete(self, id):
        cursor_obj = self.con.cursor()

        try:
            query = 'DELETE FROM orders WHERE id = ?'
            values = (id,)
            cursor_obj.execute(query, values)

            query = 'DELETE FROM order_lines WHERE order_id = ?'
            values = (id,)
            cursor_obj.execute(query, values)

            return 'Order was deleted'

        except sqlite3.Error as e:
            print('Delete exception. {}'.format(e))
