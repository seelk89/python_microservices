from flask import Flask, jsonify, request
from product_api.data.product_repository import ProductRepo
from product_api.messages.message_listener import ProductListener

app = Flask(__name__)

# Instance of our in-memory database
product_repo = ProductRepo()
# Instance of our message-listener
message_listener_created = ProductListener(1, "create", 1)
message_listener_shipped = ProductListener(1, "shipped", 1)
message_listener_canceled = ProductListener(1, "canceled", 1)
message_listener_created.start()
message_listener_shipped.start()
message_listener_canceled.start()

@app.route('/product', methods=['GET', 'PUT', 'POST', 'DELETE'])
def device_output(*args):
    arguments = request.args

    if request.method == 'GET':

        if arguments.get('id'):
            return jsonify(product_repo.get_product_by_id(arguments.get('id')))
        else:
            return jsonify(product_repo.get_all_products())

    if request.method == 'PUT':
        if arguments.get('id'):
            return product_repo.update_product(request.json, arguments.get('id'))
        else:
            'Id needed'

    if request.method == 'POST':
        return product_repo.create_product(request.json)

    if request.method == 'DELETE':
        if arguments.get('id'):
            return product_repo.delete_product(arguments.get('id'))
        else:
            'Id needed'


app.run(host='127.0.0.1', port=5002)
