import sqlite3
from datetime import date
from sqlite3 import Error


class OrderDb:
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
            cursor_obj.execute('CREATE TABLE orders (id integer PRIMARY KEY, date text, customer_id integer, order_status text, order_lines integer)')

            self.con.commit()

            cursor_obj.execute('CREATE TABLE order_lines(id integer PRIMARY KEY, order_id integer, product_id integer, quantity integer)')

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
            #query = 'SELECT * FROM orders JOIN order_lines ON order.order_lines = order_lines.order_id'
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

    def insert(self, date, customer_id, order_lines_product_id, order_lines_quantity):
        cursor_obj = self.con.cursor()

        try:
            query = 'INSERT INTO orders (date, customer_id, order_status) VALUES (?, ?, ?)'
            values = (date, customer_id, 'shipped', )
            cursor_obj.execute(query, values)

            new_order_id = cursor_obj.lastrowid
            query = 'INSERT INTO order_lines (order_id, product_id, quantity) VALUES (?, ?, ?)'
            values = (new_order_id, order_lines_product_id, order_lines_quantity,)
            cursor_obj.execute(query, values)

            new_order_lines_id = cursor_obj.lastrowid
            query = 'UPDATE orders SET order_lines = ? WHERE id = ?'
            values = (new_order_lines_id, new_order_id, )
            cursor_obj.execute(query, values)

            return 'Order was created'

        except sqlite3.Error as e:
            print('Insert exception. {}'.format(e))

    def delete(self, id):
        cursor_obj = self.con.cursor()

        try:
            # Should delete order_lines belonging to the order aswell
            query = 'DELETE FROM orders WHERE id = ?'
            values = (id,)
            cursor_obj.execute(query, values)

            return 'Order was deleted'

        except sqlite3.Error as e:
            print('Delete exception. {}'.format(e))
