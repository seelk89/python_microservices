import json
from aifc import Error
from product_api.data.product_db import ProductDb


class ProductRepo:
    __product_db: ProductDb

    def __init__(self):
        try:
            self.__product_db = ProductDb()
        except Error:
            print(Error)

    def get_all_products(self):
        # convert list to json
        product_list_json = json.dumps(self.__product_db.get_all())
        return product_list_json

    def get_product_by_id(self, product_id):
        return self.__product_db.get_by_id(product_id)

    def update_product(self, product_json):
        return self.__product_db.update(product_json["name"], product_json["price"], product_json["items_in_stock"], product_json["items_reserved"], product_json["id"])

    def create_product(self, product_json):
        return self.__product_db.insert(product_json["name"], product_json["price"], product_json["items_in_stock"], product_json["items_reserved"])

    def delete_product(self, product_id):
        return self.__product_db.delete(product_id)