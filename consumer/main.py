import json
import pika
import sys

def handler(event, context):
    """
    This function will handle the event whether it comes from AWS Lambda (SQS) or RabbitMQ
    """
    try:
        for record in event['Records']:
          message_body = json.loads(record['body'])
          journey_id = message_body['journey_id']
          print(f"Handling journey_id: {journey_id}")
          
          # TODO: Manage the event here
          
          print("Event processed successfully.")
        
    except Exception as e:
        print(f"Error processing event: {e}")


def consume_from_rabbitmq(rabbitmq_host: str):
    """
    Consume messages from RabbitMQ and pass the events to the handler
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()

    channel.exchange_declare(exchange='event_exchange', exchange_type='fanout')

    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='event_exchange', queue=queue_name)

    print(' [*] Waiting for events. To exit press CTRL+C')

    def event_callback(ch, method, properties, body):
        """
        This function will be called when a message is received from RabbitMQ.
        Then it passes the message to the handler.
        """
        try:
            message = json.loads(body)
            print(f" [x] Received events: {message}")

            # Call the handler with the event and a fictitious context
            # Here we simulate an AWS Lambda context
            event = {"Records": [{"body": body}]}  # This would be the SQS event
            context = {}  # This could be an object with details of the Lambda execution
            handler(event, context)  # Call the handler

        except Exception as e:
            print(f"Error processing message: {e}")
        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=queue_name, on_message_callback=event_callback)

    channel.start_consuming()


def lambda_handler(event, context):
    """
    This function will be used by AWS Lambda, taking the event from SQS
    """
    handler(event, context)


if __name__ == "__main__":
    # If we run this script locally, consume from RabbitMQ
    if len(sys.argv) > 1 and sys.argv[1] == "rabbitmq":
        consume_from_rabbitmq('localhost') 
    else:
        print("No RabbitMQ consumer running.")
