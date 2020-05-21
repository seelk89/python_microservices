import json
from aifc import Error
from customer_api.data.customer_db import CustomerDb
from customer_api.messages.message_publisher import CustomerPublisher


class CustomerRepo:
    __customer_db: CustomerDb
    customer_publisher = CustomerPublisher()

    def __init__(self):
        try:
            self.__customer_db = CustomerDb()
        except Error:
            print(Error)

    def get_all_customers(self):
        # convert list to json
        product_list_json = self.__customer_db.get_all()
        return product_list_json

    def get_customer_by_id(self, customer_id):
        return self.__customer_db.get_by_id(customer_id)

    def update_customer(self, customer_json, customer_id):
        return self.__customer_db.update(customer_json['name'], customer_json['email'], customer_json['phone_number'],
                                         customer_json['billing_address'], customer_json['shipping_address'],
                                         customer_json['credit_standing'], customer_id)

    def create_customer(self, customer_json):
        return self.__customer_db.insert(customer_json['name'], customer_json['email'], customer_json['phone_number'],
                                         customer_json['billing_address'], customer_json['shipping_address'],
                                         customer_json['credit_standing'])

    def delete_customer(self, customer_id):
        return self.__customer_db.delete(customer_id)

    def check_credit_standing(self, order_json):
        customer = self.get_customer_by_id(order_json["customer_id"])
        customer = customer[0]
        if customer:
            if customer['credit_standing'] == 'good':
                customer['credit_standing'] = "bad"
                self.__customer_db.update(customer["name"], customer["email"], customer["phone_number"],
                                          customer["billing_address"], customer["shipping_address"],
                                          'bad', customer["id"])
                self.customer_publisher.order_accepted(order_json)
            else:
                self.customer_publisher.order_rejected(order_json)

    def reject_order(self, order_json):
        customer = self.get_customer_by_id(order_json["customer_id"])
        customer = customer[0]
        customer['credit_standing'] = "good"
        self.__customer_db.update(customer["name"], customer["email"], customer["phone_number"],
                                  customer["billing_address"], customer["shipping_address"],
                                  customer["credit_standing"], customer["id"])
        self.customer_publisher.order_rejected(order_json)

    def status_change(self, order_json):
        customer = self.get_customer_by_id(order_json["customer_id"])
        customer = customer[0]

        customer['credit_standing'] = "good"
        self.__customer_db.update(customer["name"], customer["email"], customer["phone_number"],
                                  customer["billing_address"], customer["shipping_address"],
                                  "bad", customer["id"])
