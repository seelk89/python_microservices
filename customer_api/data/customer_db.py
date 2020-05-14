import sqlite3
from sqlite3 import Error


class CustomerDb:
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
                'CREATE TABLE customers (id integer PRIMARY KEY, name text, email text, phone_number text, billing_address text, shipping_address text, credit_standing text)')

            self.con.commit()

            print('Table created')

        except sqlite3.Error as e:
            print('Table creation exception. {}'.format(e))

    def __seed_db(self):
        cursor_obj = self.con.cursor()

        try:
            insert_query = 'INSERT INTO customers (name, email, phone_number, billing_address, shipping_address, credit_standing) VALUES (?, ?, ?, ?, ?, ?)'

            values = ('customer1', 'email1@email.com', '12345678', 'billing_address1', 'shipping_address1', 'good',)
            cursor_obj.execute(insert_query, values)

            values = ('customer2', 'email2@email.com', '87654321', 'billing_address2', 'shipping_address2', 'bad',)
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
            query = 'SELECT * FROM customers'
            cursor_obj.execute(query)

            query_result = cursor_obj.fetchall()

            return query_result

        except sqlite3.Error as e:
            print('Select exception. {}'.format(e))

    def get_by_id(self, id):
        cursor_obj = self.con.cursor()

        try:
            query = 'SELECT * FROM customers WHERE id = ?'
            value = (id,)
            cursor_obj.execute(query, value,)

            query_result = cursor_obj.fetchall()

            return query_result

        except sqlite3.Error as e:
            print('Select exception. {}'.format(e))

    def update(self, name, email, phone_number, billing_address, shipping_address, credit_standing, id):
        cursor_obj = self.con.cursor()

        try:
            query = 'UPDATE customers SET date = ?, customer_id = ?, order_lines = ? WHERE id = ?'
            values = (name, email, phone_number, billing_address, shipping_address, credit_standing, id,)
            cursor_obj.execute(query, values)

            return 'Customer was updated'

        except sqlite3.Error as e:
            print('Update exception. {}'.format(e))

    def insert(self, name, email, phone_number, billing_address, shipping_address, credit_standing):
        cursor_obj = self.con.cursor()

        try:
            query = 'INSERT INTO customers (date, customer_id, order_lines) VALUES (?, ?, ?)'
            values = (name, email, phone_number, billing_address, shipping_address, credit_standing,)
            cursor_obj.execute(query, values)

            return 'Customer was created'

        except sqlite3.Error as e:
            print('Insert exception. {}'.format(e))

    def delete(self, id):
        cursor_obj = self.con.cursor()

        try:
            query = 'DELETE FROM customers WHERE id = ?'
            values = (id,)
            cursor_obj.execute(query, values)

            return 'Customer was deleted'

        except sqlite3.Error as e:
            print('Delete exception. {}'.format(e))
