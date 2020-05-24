import requests
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/gateway', methods=['GET', 'PUT', 'POST', 'DELETE'])
def device_output(*args):
    arguments = request.args

    # Order api
    if arguments.get('api') == 'order':
        if request.method == 'GET':
            if arguments.get('id'):
                return jsonify(requests.get('http://python_microservices_order_api_1:5000/order', params={'id': arguments.get('id')}).json())
            else:
                return jsonify(requests.get('http://python_microservices_order_api_1:5000/order').json())

        if request.method == 'PUT':
            if arguments.get('id'):
                request_json = request.json
                requests.put('http://python_microservices_order_api_1:5000/order', params={'id': arguments.get('id')},
                             json={'date': request_json['date'], 'customer_id': request_json['customer_id'],
                                   'order_lines': request_json['order_lines']})
            else:
                'Id needed'

        if request.method == 'POST':
            request_json = request.json
            return requests.post('http://python_microservices_order_api_1:5000/order',
                          json={'date': request_json['date'], 'customer_id': request_json['customer_id'],
                                'order_lines': request_json['order_lines']})

        if request.method == 'DELETE':
            if arguments.get('id'):
                requests.delete('http://python_microservices_order_api_1:5000/order', params={'id': arguments.get('id')})
            else:
                'Id needed'

    # Product api
    if arguments.get('api') == 'product':
        if request.method == 'GET':
            if arguments.get('id'):
                return jsonify(requests.get('http://python_microservices_product_api_1:5002/product', params={'id': arguments.get('id')}).json)
            else:
                return jsonify(requests.get('http://python_microservices_product_api_1:5002/product').json())

        if request.method == 'PUT':
            if arguments.get('id'):
                request_json = request.json
                requests.put('http://python_microservices_product_api_1:5002/product', params={'id': arguments.get('id')},
                             json={'name': request.json['name'], 'price': request_json['price'],
                                   'items_in_stock': request_json['items_in_stock'],
                                   'items_reserved': request_json['items_reserved']})
            else:
                'Id needed'

        if request.method == 'POST':
            request_json = request.json
            requests.put('http://python_microservices_product_api_1:5002/product',
                         json={'name': request.json['name'], 'price': request_json['price'],
                               'items_in_stock': request_json['items_in_stock'],
                               'items_reserved': request_json['items_reserved']})

        if request.method == 'DELETE':
            if arguments.get('id'):
                requests.delete('http://python_microservices_product_api_1:5002/product', params={'id': arguments.get('id')})
            else:
                'Id needed'

    # Customer api
    if arguments.get('api') == 'customer':
        if request.method == 'GET':
            if arguments.get('id'):
                return jsonify(requests.get('http://python_microservices_customer_api_1:5001/customer', params={'id': arguments.get('id')}).json)
            else:
                return jsonify(requests.get('http://python_microservices_customer_api_1:5001/customer').json())

        if request.method == 'PUT':
            if arguments.get('id'):
                request_json = request.json
                requests.put('http://python_microservices_customer_api_1:5001/customer', params={'id': arguments.get('id')},
                             json={'name': request_json['name'], 'email': request_json['email'],
                                   'phone_number': request_json['phone_number'],
                                   'billing_address': request_json['billing_address'],
                                   'shipping_address': request_json['shipping_address'],
                                   'credit_standing': request_json['credit_standing']})
            else:
                "Id needed"

        if request.method == 'POST':
            request_json = request.json
            requests.put('http://0.0.0.0:5001/customer',
                         json={'name': request_json['name'], 'email': request_json['email'],
                               'phone_number': request_json['phone_number'],
                               'billing_address': request_json['billing_address'],
                               'shipping_address': request_json['shipping_address'],
                               'credit_standing': request_json['credit_standing']})

        if request.method == 'DELETE':
            if arguments.get('id'):
                requests.delete('http://0.0.0.0:5001/customer', params={'id': arguments.get('id')})
            else:
                'Id needed'


app.run(host='0.0.0.0', port=5003)
