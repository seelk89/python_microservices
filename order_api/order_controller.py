import requests
from flask import Flask, jsonify, request
from order_api.data.order_db import OrderDb
from order_api.data.order_repository import OrderRepo
from order_api.messages.message_listener import OrderListener
app = Flask(__name__)

# Instance of our in-memory database
order_repo = OrderRepo()
order_listener_create = OrderListener(1, "create", 1)
order_listener_reject = OrderListener(1, "reject", 1)
order_listener_create.start()
order_listener_reject.start()

@app.route('/order', methods=['GET', 'PUT', 'POST', 'DELETE'])
def device_output(*args):
    arguments = request.args

    if request.method == 'GET':
        if arguments.get('id'):
            return jsonify(order_repo.get_order_by_id(arguments.get('id')))
        else:
            return jsonify(order_repo.get_all_orders())

    if request.method == 'PUT':
        if arguments.get('id'):
            request_json = request.json
            return order_repo.update_order(request_json, arguments.get('id'))
        else:
            'Id needed'

    if request.method == 'POST':
        request_json = request.json
        return order_repo.create_order(request.json)

    if request.method == 'DELETE':
        if arguments.get('id'):
            return order_repo.delete_order(arguments.get('id'))
        else:
            'Id needed'

    if arguments.get('state') == 'cancel':
        if request.method == 'GET':
            if arguments.get('id'):
                return order_repo.cancel_order(arguments.get('id'))

    if arguments.get('state') == 'ship':
        if request.method == 'GET':
            if arguments.get('id'):
                return order_repo.ship_order(arguments.get('id'))

app.run(host='127.0.0.1')
