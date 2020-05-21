import json
import threading
from product_api.data.product_repository import ProductRepo

import pika, os


class ProductListener(threading.Thread):
    product_repo = ProductRepo()


    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        if self.name == "create":
            self.order_created()
        if self.name == "shipped":
            self.order_shipped()
        if self.name == "canceled":
            self.order_canceled()

    def order_canceled(self):
        try:
            # Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
            url = os.environ.get('CLOUDAMQP_URL',
                                 'amqp://ffgzglpl:AT8pWl0aP_dfXSfKpT0pGdAms_rKSGm3@bloodhound.rmq.cloudamqp.com/ffgzglpl')
            params = pika.URLParameters(url)
            params._socket_timeout = 5
            connection = pika.BlockingConnection(params)
            channel = connection.channel()  # start a channel
            channel.queue_declare(queue='status_change')  # Declare a queue

            def callback(ch, method, properties, body):
                body = body.decode('utf-8')
                body = json.loads(body)
                self.product_repo.cancel_order(body)

            channel.basic_consume('order_cancel', callback, auto_ack=True)

            channel.start_consuming()

            connection.close()
        except Exception:
            print(Exception)

    def order_shipped(self):
        try:
            # Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
            url = os.environ.get('CLOUDAMQP_URL',
                                 'amqp://ffgzglpl:AT8pWl0aP_dfXSfKpT0pGdAms_rKSGm3@bloodhound.rmq.cloudamqp.com/ffgzglpl')
            params = pika.URLParameters(url)
            params._socket_timeout = 5
            connection = pika.BlockingConnection(params)
            channel = connection.channel()  # start a channel
            channel.queue_declare(queue='status_change')  # Declare a queue

            def callback(ch, method, properties, body):
                body = body.decode('utf-8')
                body = json.loads(body)
                self.product_repo.ship_order(body)

            channel.basic_consume('order_ship', callback, auto_ack=True)

            channel.start_consuming()

            connection.close()
        except Exception:
            print(Exception)

    def order_created(self):
        try:
            # Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
            url = os.environ.get('CLOUDAMQP_URL',
                                 'amqp://ffgzglpl:AT8pWl0aP_dfXSfKpT0pGdAms_rKSGm3@bloodhound.rmq.cloudamqp.com/ffgzglpl')
            params = pika.URLParameters(url)
            params._socket_timeout = 5
            connection = pika.BlockingConnection(params)
            channel = connection.channel()  # start a channel
            channel.queue_declare(queue='create_order')  # Declare a queue

            def callback(ch, method, properties, body):
                body = body.decode('utf-8')
                body = json.loads(body)
                self.product_repo.check_if_products_available(body)

            channel.basic_consume('check_product', callback, auto_ack=True)

            channel.start_consuming()

            connection.close()
        except Exception:
            print(Exception)