import time
import requests
from flask import Flask, request, jsonify, Response
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram,  Gauge
app = Flask(__name__)

_INF = float("inf")

graphs = {}
graphs['c'] = Counter('python_request_operations_total', 'The total number of processed requests')
graphs['h'] = Histogram('python_request_duration_seconds', 'Histogram for the duration in seconds.', buckets=(1, 2, 5, 6, 10, _INF))
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

@app.route('/gateway', methods=['GET', 'PUT', 'POST', 'DELETE'])
def device_output(*args):
    arguments = request.args

    # Order api
    if arguments.get('api') == 'order':
        if request.method == 'GET':
            if arguments.get('id'):
                start = time.time()
                graphs['c'].inc()

                response = requests.get('http://python_microservices_order_api_1:5000/order',params={'id': arguments.get('id')}).json()

                end = time.time()
                graphs['h'].observe(end - start)
                return jsonify(response)
            else:
                start = time.time()
                graphs['c'].inc()

                response = requests.get('http://python_microservices_order_api_1:5000/order').json()

                end = time.time()
                graphs['h'].observe(end - start)
                return jsonify(response)

        if request.method == 'PUT':
            if arguments.get('id'):
                request_json = request.json
                start = time.time()
                graphs['c'].inc()
                requests.put('http://python_microservices_order_api_1:5000/order', params={'id': arguments.get('id')},
                             json={'date': request_json['date'], 'customer_id': request_json['customer_id'],
                                   'order_lines': request_json['order_lines']})
                end = time.time()
                graphs['h'].observe(end - start)
            else:
                'Id needed'

        if request.method == 'POST':
            request_json = request.json
            start = time.time()
            graphs['c'].inc()
            requests.post('http://python_microservices_order_api_1:5000/order',
                          json={'date': request_json['date'], 'customer_id': request_json['customer_id'],
                                'order_lines': request_json['order_lines']})
            end = time.time()
            graphs['h'].observe(end - start)


        if request.method == 'DELETE':
            if arguments.get('id'):
                start = time.time()
                graphs['c'].inc()
                requests.delete('http://python_microservices_order_api_1:5000/order', params={'id': arguments.get('id')})
                end = time.time()
                graphs['h'].observe(end - start)
            else:
                'Id needed'

    # Product api
    if arguments.get('api') == 'product':
        if request.method == 'GET':
            if arguments.get('id'):
                start = time.time()
                graphs['c'].inc()
                response = requests.get('http://python_microservices_product_api_1:5002/product',
                             params={'id': arguments.get('id')}).json()
                end = time.time()
                graphs['h'].observe(end - start)
                return jsonify(response)
            else:
                start = time.time()
                graphs['c'].inc()
                response = requests.get('http://python_microservices_product_api_1:5002/product').json()
                end = time.time()
                graphs['h'].observe(end - start)
                return jsonify(response)

        if request.method == 'PUT':
            if arguments.get('id'):
                request_json = request.json
                start = time.time()
                graphs['c'].inc()
                requests.put('http://python_microservices_product_api_1:5002/product', params={'id': arguments.get('id')},
                             json={'name': request.json['name'], 'price': request_json['price'],
                                   'items_in_stock': request_json['items_in_stock'],
                                   'items_reserved': request_json['items_reserved']})
                end = time.time()
                graphs['h'].observe(end - start)
            else:
                'Id needed'

        if request.method == 'POST':
            request_json = request.json
            start = time.time()
            graphs['c'].inc()
            requests.put('http://python_microservices_product_api_1:5002/product',
                         json={'name': request.json['name'], 'price': request_json['price'],
                               'items_in_stock': request_json['items_in_stock'],
                               'items_reserved': request_json['items_reserved']})
            end = time.time()
            graphs['h'].observe(end - start)

        if request.method == 'DELETE':
            if arguments.get('id'):
                start = time.time()
                graphs['c'].inc()
                requests.delete('http://python_microservices_product_api_1:5002/product', params={'id': arguments.get('id')})
                end = time.time()
                graphs['h'].observe(end - start)
            else:
                'Id needed'

    # Customer api
    if arguments.get('api') == 'customer':
        if request.method == 'GET':
            if arguments.get('id'):
                start = time.time()
                graphs['c'].inc()
                return jsonify(requests.get('http://python_microservices_customer_api_1:5001/customer', params={'id': arguments.get('id')}).json)
            else:
                start = time.time()
                graphs['c'].inc()
                all_customers = requests.get('http://python_microservices_customer_api_1:5001/customer').json()
                end = time.time()
                graphs['h'].observe(end - start)
                return jsonify(all_customers)

        if request.method == 'PUT':
            if arguments.get('id'):
                request_json = request.json
                start = time.time()
                graphs['c'].inc()
                requests.put('http://python_microservices_customer_api_1:5001/customer', params={'id': arguments.get('id')},
                             json={'name': request_json['name'], 'email': request_json['email'],
                                   'phone_number': request_json['phone_number'],
                                   'billing_address': request_json['billing_address'],
                                   'shipping_address': request_json['shipping_address'],
                                   'credit_standing': request_json['credit_standing']})
                end = time.time()
                graphs['h'].observe(end - start)
            else:
                "Id needed"

        if request.method == 'POST':
            request_json = request.json
            start = time.time()
            graphs['c'].inc()
            requests.put('http://python_microservices_customer_api_1:5001/customer',
                         json={'name': request_json['name'], 'email': request_json['email'],
                               'phone_number': request_json['phone_number'],
                               'billing_address': request_json['billing_address'],
                               'shipping_address': request_json['shipping_address'],
                               'credit_standing': request_json['credit_standing']})
            end = time.time()
            graphs['h'].observe(end - start)

        if request.method == 'DELETE':
            if arguments.get('id'):
                start = time.time()
                graphs['c'].inc()
                requests.delete('http://0.0.0.0:5001/customer', params={'id': arguments.get('id')})
                end = time.time()
                graphs['h'].observe(end - start)
            else:
                'Id needed'

@app.route("/metrics")
def requests_count():
    res = []
    for k,v in graphs.items():
        res.append(prometheus_client.generate_latest(v))
    return Response(res, mimetype="text/plain")
app.run(host='0.0.0.0', port=5003)
