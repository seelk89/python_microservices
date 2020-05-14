from flask import Flask, jsonify, request
from customer_api.data.customer_db import CustomerDb

app = Flask(__name__)

# Instance of our in-memory database
customer_db = CustomerDb()


@app.route('/customer', methods=['GET', 'PUT', 'POST', 'DELETE'])
def device_output(*args):
    arguments = request.args

    if request.method == 'GET':
        if arguments.get('id'):
            return jsonify(customer_db.get_by_id(arguments.get('id')))
        else:
            return jsonify(customer_db.get_all())

    if request.method == 'PUT':
        if arguments.get('id'):
            request_json = request.json
            return customer_db.update(request_json['name'], request_json['email'], request_json['phone_number'], request_json['billing_address'], request_json['shipping_address'], request_json['credit_standing'], arguments.get('id'))
        else:
            "Id needed"

    if request.method == 'POST':
        request_json = request.json
        return customer_db.insert(request_json['name'], request_json['email'], request_json['phone_number'], request_json['billing_address'], request_json['shipping_address'], request_json['credit_standing'])

    if request.method == 'DELETE':
        if arguments.get('id'):
            return customer_db.delete(arguments.get('id'))
        else:
            'Id needed'


app.run(host='127.0.0.1', port=5001)
