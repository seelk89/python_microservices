from aifc import Error

from data.order_db import OrderDb
from messages.message_publisher import OrderPublisher


class OrderRepo:
    __order_db: OrderDb
    order_publisher = OrderPublisher()

    def __init__(self):
        try:
            self.__order_db = OrderDb()
        except Error:
            print(Error)

    def get_all_orders(self):
        # convert list to json
        order_list_json = self.__order_db.get_all()
        return order_list_json

    def get_order_by_id(self, order_id):
        return self.__order_db.get_by_id(order_id)

    def update_order(self, order_json, order_id):
        return self.__order_db.update(order_json['date'], order_json['customer_id'], order_json['order_status'],
                                      order_id)

    def create_order(self, order_json):
        returned_id = self.__order_db.insert(order_json['date'], order_json['customer_id'], 'pending',
                                             order_json['order_lines'])
        order_json['id'] = returned_id
        self.order_publisher.create_order(order_json)
        return order_json

    def delete_order(self, id):
        return self.__order_db.delete(id)

    def reject_order(self, order_json):
        return self.__order_db.update(order_json['date'], order_json['customer_id'], 'rejected', order_json['id'])

    def accept_order(self, order_json):
        order_to_ship = self.get_order_by_id(int(order_json['id']))
        order_to_ship = order_to_ship[0]
        order_to_ship['order_status'] = 'created'
        return self.update_order(order_to_ship, order_json['id'])

    def cancel_order(self, order_id):
        order_to_cancel = self.get_order_by_id(order_id)
        if order_to_cancel[0]['order_status'] == 'created':
            order_to_cancel[0]['order_status'] = 'canceled'
            self.update_order(order_to_cancel[0], order_id)
            self.order_publisher.cancel_order(order_to_cancel)

    def ship_order(self, order_id):
        order_to_ship = self.get_order_by_id(order_id)
        order_to_ship = order_to_ship[0]
        if order_to_ship['order_status'] == 'created':
            order_to_ship['order_status'] = 'shipped'
            self.update_order(order_to_ship, order_id)
            self.order_publisher.ship_order(order_to_ship)
