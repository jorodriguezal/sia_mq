#!/usr/bin/env python
import pika
import requests
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='127.0.0.1'))


channel = connection.channel()

channel.queue_declare(queue='rpc_queue')


def on_request(ch, method, props, body):
    print(" [.] Inscripción(%s)" % body)
    response = requests.post('http://localhost:4000/inscripcion', data=body)
    # form a json with the code and the message
    response = json.dumps(
        {"code": response.status_code, "message": response.text})

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(
                         correlation_id=props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()
