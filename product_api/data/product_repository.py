import json
from aifc import Error

from product_api.data.product_db import ProductDb
from product_api.messages.message_publisher import ProductPublisher


class ProductRepo:
    __product_db: ProductDb()
    product_publisher = ProductPublisher()

    def __init__(self):
        try:
            self.__product_db = ProductDb()
        except Error:
            print(Error)

    def get_all_products(self):
        # convert list to json
        product_list_json = self.__product_db.get_all()
        return product_list_json

    def get_product_by_id(self, product_id):
        return self.__product_db.get_by_id(product_id)

    def update_product(self, product_json, product_id):
        return self.__product_db.update(product_json['name'], product_json['price'], product_json['items_in_stock'],
                                        product_json['items_reserved'], product_id)

    def create_product(self, product_json):
        return self.__product_db.insert(product_json["name"], product_json["price"], product_json["items_in_stock"],
                                        product_json["items_reserved"])

    def delete_product(self, product_id):
        return self.__product_db.delete(product_id)

    def check_if_products_available(self, order_json):
        for order_line in order_json["order_lines"]:
            product = self.__product_db.get_by_id(order_line["product_id"])

            if int(product[0]["items_in_stock"]) < int(order_line["quantity"]):
                self.reject_order(order_json)
                return "no good"

        for order_line in order_json["order_lines"]:
            product = self.__product_db.get_by_id(order_line["product_id"])
            product[0]["items_in_stock"] = int(product[0]["items_in_stock"]) - int(order_line["quantity"])
            product[0]["items_reserved"] = int(product[0]["items_reserved"]) + int(order_line["quantity"])
            self.update_product(product[0], product[0]["id"])
        self.accept_order(order_json)

    def accept_order(self, order_json):
        self.product_publisher.order_accepted(order_json)

    def reject_order(self, order_json):
        self.product_publisher.order_rejected(order_json)

    def ship_order(self, order_json):
        for order_line in order_json["order_lines"]:
            product = self.__product_db.get_by_id(order_line["product_id"])
            product[0]["items_reserved"] = int(product[0]["items_reserved"]) - int(order_line["quantity"])
            self.update_product(product[0], product[0]["id"])

    def cancel_order(self, order_json):
        for order_line in order_json["order_lines"]:
            product = self.__product_db.get_by_id(order_line["product_id"])
            product[0]["items_in_stock"] = int(product[0]["items_in_stock"]) + int(order_line["quantity"])
            product[0]["items_reserved"] = int(product[0]["items_reserved"]) - int(order_line["quantity"])
            self.update_product(product[0], product[0]["id"])
