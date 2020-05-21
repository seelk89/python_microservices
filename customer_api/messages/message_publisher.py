import json

import pika, os
from pika import BlockingConnection, URLParameters


class CustomerPublisher:
    params: URLParameters

    def __init__(self):
        try:
            # Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
            url = os.environ.get('CLOUDAMQP_URL',
                                 'amqp://ffgzglpl:AT8pWl0aP_dfXSfKpT0pGdAms_rKSGm3@bloodhound.rmq.cloudamqp.com/ffgzglpl')
            self.params = pika.URLParameters(url)
        except Exception:
            print(Exception)

    def order_accepted(self, order_json):
        connection = pika.BlockingConnection(self.params)
        channel = connection.channel()  # start a channel
        channel.queue_declare(queue='create_order')  # Declare a queue
        channel.basic_publish(exchange='',
                              routing_key='check_product',
                              body=json.dumps(order_json))

        print(" [x] Sent 'Hello World!'")
        connection.close()

    def order_rejected(self, order_json):
        connection = pika.BlockingConnection(self.params)
        channel = connection.channel()  # start a channel
        channel.queue_declare(queue='create_order')  # Declare a queue
        channel.basic_publish(exchange='',
                              routing_key='order_rejected',
                              body=json.dumps(order_json))

        print(" [x] Sent 'Hello World!'")
        connection.close()
