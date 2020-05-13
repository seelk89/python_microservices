from os import abort

from flask import Flask, jsonify, request
from order_api.data.order_db import OrderDb

app = Flask(__name__)

# Instance of our in-memory database
order_db = OrderDb()


@app.route('/order', methods=['GET', 'PUT', 'POST', 'DELETE'])
def device_output(*args):
    arguments = request.args

    if request.method == 'GET':
        if arguments.get('id'):
            return jsonify(order_db.get_by_id(arguments.get('id')))
        else:
            return order_db.get_all()

    if request.method == 'PUT':
        if arguments.get('id'):
            request_json = request.json
            return order_db.update(request_json['date'], request_json['customer_id'], request_json['order_lines'], arguments.get('id'))
        else:
            "Id needed"

    if request.method == 'POST':
        request_json = request.json
        return order_db.insert(request_json['date'], request_json['customer_id'], request_json['order_lines'])
    if request.method == 'DELETE':
        return order_db.delete(arguments.get('id'))


app.run(host='0.0.0.0')
