from flask import Flask, jsonify, request
from product_api.data.product_db import ProductDb

app = Flask(__name__)

# Instance of our in-memory database
product_repo = ProductDb()


@app.route('/product', methods=['GET', 'PUT', 'POST', 'DELETE'])
def device_output(*args):
    arguments = request.args

    if request.method == 'GET':

        if arguments.get('id'):
            return jsonify(product_repo.get_by_id(arguments.get('id')))
        else:
            return jsonify(product_repo.get_all())

    if request.method == 'PUT':
        if arguments.get('id'):
            return product_repo.update(request.json['name'], request.json['price'], request.json['items_in_stock'], request.json['items_reserved'])
        else:
            'Id needed'

    if request.method == 'POST':
        return product_repo.insert(request.json['name'], request.json['price'], request.json['items_in_stock'], request.json['items_reserved'])

    if request.method == 'DELETE':
        if arguments.get('id'):
            return product_repo.delete(arguments.get('id'))
        else:
            'Id needed'


app.run(host='0.0.0.0', port=5002)
