from flask import Flask, jsonify, request
from customer_api.data.customer_repository import CustomerRepo
from customer_api.messages.message_listener import CustomerListener

app = Flask(__name__)

# Instance of our in-memory database
customer_repo = CustomerRepo()
customer_listener_create = CustomerListener(1, "create", 1)
customer_listener_reject = CustomerListener(1, "reject", 1)
customer_listener_shipped = CustomerListener(1, "shipped", 1)
customer_listener_canceled = CustomerListener(1, "canceled", 1)
customer_listener_create.start()
customer_listener_reject.start()
customer_listener_canceled.start()
customer_listener_shipped.start()


@app.route('/customer', methods=['GET', 'PUT', 'POST', 'DELETE'])
def device_output(*args):
    arguments = request.args

    if request.method == 'GET':
        if arguments.get('id'):
            return jsonify(customer_repo.get_customer_by_id(arguments.get('id')))
        else:
            return jsonify(customer_repo.get_all_customers())

    if request.method == 'PUT':
        if arguments.get('id'):
            request_json = request.json
            return customer_repo.update_customer(request_json, arguments.get('id'))
        else:
            "Id needed"

    if request.method == 'POST':
        request_json = request.json
        return customer_repo.create_customer(request_json)

    if request.method == 'DELETE':
        if arguments.get('id'):
            return customer_repo.delete_customer(arguments.get('id'))
        else:
            'Id needed'


app.run(host='127.0.0.1', port=5001)
