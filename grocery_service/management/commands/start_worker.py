#!/usr/bin/env python

import pika, sys

from grocery_service.models import GroceryList, Store

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='some-rabbit'))
channel = connection.channel()

channel.exchange_declare(exchange='new_user', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

    
channel.queue_bind(exchange='new_user', queue=queue_name)
print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")
    stores_list = Store.objects.all()
    for store in stores_list:
        GroceryList.objects.create(
            user = body,
            store = store
        )


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()