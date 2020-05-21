import json

import pika, os
from pika import BlockingConnection, URLParameters


class OrderPublisher:

    def create_order(self, order_json):
        # Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
        url = os.environ.get('CLOUDAMQP_URL', 'amqp://ffgzglpl:AT8pWl0aP_dfXSfKpT0pGdAms_rKSGm3@bloodhound.rmq.cloudamqp.com/ffgzglpl')
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()  # start a channel
        channel.queue_declare(queue='create_order')  # Declare a queue
        channel.basic_publish(exchange='',
                              routing_key='check_customer',
                              body=json.dumps(order_json))

        print("Sent customer validation")
        connection.close()

    def cancel_order(self, order_json):
        # Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
        url = os.environ.get('CLOUDAMQP_URL',
                             'amqp://ffgzglpl:AT8pWl0aP_dfXSfKpT0pGdAms_rKSGm3@bloodhound.rmq.cloudamqp.com/ffgzglpl')
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()  # start a channel
        channel.queue_declare(queue='change_status')  # Declare a queue
        channel.basic_publish(exchange='',
                              routing_key='order_cancel',
                              body=json.dumps(order_json))

        print("Sent customer validation")
        connection.close()

    def ship_order(self, order_json):
        # Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
        url = os.environ.get('CLOUDAMQP_URL',
                             'amqp://ffgzglpl:AT8pWl0aP_dfXSfKpT0pGdAms_rKSGm3@bloodhound.rmq.cloudamqp.com/ffgzglpl')
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()  # start a channel
        channel.queue_declare(queue='change_status')  # Declare a queue
        channel.basic_publish(exchange='',
                              routing_key='order_ship',
                              body=json.dumps(order_json))

        print("Sent customer validation")
        connection.close()
