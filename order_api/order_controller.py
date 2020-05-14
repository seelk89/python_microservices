import requests
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
            return jsonify(order_db.get_all())

    if request.method == 'PUT':
        if arguments.get('id'):
            request_json = request.json
            return order_db.update(request_json['date'], request_json['customer_id'], request_json['order_lines'],
                                   arguments.get('id'))
        else:
            'Id needed'

    if request.method == 'POST':
        request_json = request.json

        req_pro_api = requests.get('http://127.0.0.1:5002/product', params={'id': request_json['order_lines']['product_id']})
        if req_pro_api.json()[0]['items_in_stock'] > request_json['order_lines']['quantity']:
            print('Items are in stock')

            req_cus_api = requests.get('http://127.0.0.1:5001/customer', params={'id': request_json['customer_id']})
            if req_cus_api:
                print('Customer exists')

                if req_cus_api.json()[0]['credit_standing'] == 'good':
                    print('Customer credit standing is good')

                    return order_db.insert(request_json['date'], request_json['customer_id'], request_json['order_lines']['product_id'], request_json['order_lines']['quantity'])
                else:
                    print('Customer credit standing is bad')
            else:
                print('The customer does not exist')
        else:
            print('Items are not in stock')

    if request.method == 'DELETE':
        if arguments.get('id'):
            return order_db.delete(arguments.get('id'))
        else:
            'Id needed'


app.run(host='127.0.0.1')
