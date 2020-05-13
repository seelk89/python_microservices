import json
from flask import Flask, jsonify, request
from product_api.data.product_repository import ProductRepo

app = Flask(__name__)


@app.route('/product', methods=['GET', 'PUT', 'POST', 'DELETE'])
def device_output(*args):
    arguments = request.args
    product_repo = ProductRepo()

    if request.method == 'GET':

        if arguments.get('id'):
            return jsonify(product_repo.get_product_by_id(arguments.get('id')))
        else:
            return product_repo.get_all_products()

    if request.method == 'PUT':
        return product_repo.update_product(request.json)

    if request.method == 'POST':
        return product_repo.create_product(request.json)

    if request.method == 'DELETE':
        return product_repo.delete_product(arguments.get('id'))


app.run(host='0.0.0.0')
