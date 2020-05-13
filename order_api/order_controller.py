import json
from flask import Flask, jsonify, request
from order_api.data.order_repository import OrderRepo

app = Flask(__name__)


@app.route('/order', methods=['GET', 'PUT', 'POST', 'DELETE'])
def device_output(*args):
    arguments = request.args
    order_repo = OrderRepo()

    if request.method == 'GET':

        if arguments.get('id'):
            return jsonify(order_repo.get_order_by_id(arguments.get('id')))
        else:
            return order_repo.get_all_orders()

    if request.method == 'PUT':
        return order_repo.update_order(request.json)

    if request.method == 'POST':
        return order_repo.create_order(request.json)

    if request.method == 'DELETE':
        return order_repo.delete_order(arguments.get('id'))


app.run(host='0.0.0.0')
