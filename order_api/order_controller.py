from flask import Flask, jsonify, request

from order_db import OrderDb

app = Flask(__name__)


@app.route('/order', methods=['GET', 'PUT', 'POST', 'DELETE'])
def device_output(*args):
    arguments = request.args
    db = OrderDb()

    if request.method == 'GET':
        if arguments.get('order_id'):
            return jsonify(db.get_by_id(arguments.get('id')))

        else:
            return db.get_by_id(db.get_all())

    if request.method == 'PUT':
        db.update(request.json)

    if request.method == 'POST':
        db.insert(request.json)

    if request.method == 'DELETE':
        db.delete(request.json)


app.run(host='0.0.0.0')
