import sqlite3
from datetime import datetime
from sqlite3 import Error


class OrderDb:
    def __init__(self):
        try:
            self.con = sqlite3.connect(':memory:')

            print('Database created in-memory')

            self.__create_sqlite_tables()

            self.__seed_db()

        except Error:
            print(Error)

    def __create_sqlite_tables(self):
        cursor_obj = self.con.cursor()

        try:
            cursor_obj.execute('CREATE TABLE orders (id integer PRIMARY KEY, date text, customer_id integer, order_status text, order_lines integer)')

            self.con.commit()

            cursor_obj.execute('CREATE TABLE order_lines(id integer PRIMARY KEY, order_id integer, product_id integer, quantity integer)')

            self.con.commit()

            print('Tables created')

        except sqlite3.Error as e:
            print('Table creation exception. {}'.format(e))

    def __seed_db(self):
        cursor_obj = self.con.cursor()

        try:
            insert_query = 'INSERT INTO orders (date, customer_id, order_lines) VALUES (?, ?, ?)'

            values = (str(datetime.now), 1, 1,)
            cursor_obj.execute(insert_query, values)

            values = (str(datetime.now), 2, 1,)
            cursor_obj.execute(insert_query, values)

            insert_query = 'INSERT INTO order_lines (order_id, product_id, quantity) VALUES (?, ?, ?)'
            values = (1, 1, 10,)

            cursor_obj.execute(insert_query, values)

            print('Db seeded')

        except sqlite3.Error as e:
            print('Insert exception. {}'.format(e))

    def get_all(self):
        cursor_obj = self.con.cursor()

        try:
            query = 'SELECT * FROM orders'
            cursor_obj.execute(query)

            query_result = cursor_obj.fetchall()

            return query_result

        except sqlite3.Error as e:
            print('Select exception. {}'.format(e))

    def get_by_id(self, id):
        cursor_obj = self.con.cursor()

        try:
            query = 'SELECT * FROM orders WHERE id = ?'
            value = (id,)
            cursor_obj.execute(query, value,)

            query_result = cursor_obj.fetchall()

            return query_result

        except sqlite3.Error as e:
            print('Select exception. {}'.format(e))

    def update(self, date, customer_id, order_lines, id):
        cursor_obj = self.con.cursor()

        try:
            query = 'UPDATE orders SET date = ?, customer_id = ?, order_lines = ? WHERE id = ?'
            values = (date, customer_id, order_lines, id, )
            cursor_obj.execute(query, values)

            return 'Order was updated'

        except sqlite3.Error as e:
            print('Update exception. {}'.format(e))

    def insert(self, date, customer_id, order_lines):
        cursor_obj = self.con.cursor()

        try:
            query = 'INSERT INTO orders (date, customer_id, order_lines) VALUES (?, ?, ?)'
            values = (date, customer_id, order_lines, )
            cursor_obj.execute(query, values)

            return 'Order was created'

        except sqlite3.Error as e:
            print('Insert exception. {}'.format(e))

    def delete(self, id):
        cursor_obj = self.con.cursor()

        try:
            query = 'DELETE FROM orders WHERE id = ?'
            values = (id,)
            cursor_obj.execute(query, values)

            return 'Order was deleted'

        except sqlite3.Error as e:
            print('Delete exception. {}'.format(e))
