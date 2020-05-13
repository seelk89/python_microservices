import json
from aifc import Error
from order_api.data.order_db import OrderDb


class OrderRepo:
    __order_db: OrderDb

    def __init__(self):
        try:
            self.__order_db = OrderDb()
        except Error:
            print(Error)

    def get_all_orders(self):
        # convert list to json
        order_list_json = json.dumps(self.__order_db.get_all())
        return order_list_json

    def get_order_by_id(self, id):
        return self.__order_db.get_by_id(id)

    def update_order(self, order_json):
        return self.__product_db.update(order_json["date"], order_json["customer_id"], order_json["order_lines"], order_json["id"])

    def create_order(self, order_json):
        return self.__product_db.insert(order_json["date"], order_json["customer_id"], order_json["order_lines"])

    def delete_order(self, id):
        return self.__order_db.delete(id)