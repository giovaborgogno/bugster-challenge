import json
import boto3
import sys
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def handler(event, context):
    """
    This function will handle the event whether it comes from AWS Lambda (SQS) or from the local consumer
    """
    try:
        for record in event['Records']:
            message_body = json.loads(record['body'])
            journey_id = message_body['journey_id']
            logger.info(f"Handling journey_id: {journey_id}")
            
            # TODO: Manage the event here
            
            logger.info("Event processed successfully.")
        
    except Exception as e:
        logger.error(f"Error processing event: {e}")

def consume_from_sqs():
    """"
    Consume messages from SQS and pass the events to the handler
    """
    load_dotenv()

    # Access environment variables
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    SQS_ENDPOINT_URL = os.getenv('SQS_ENDPOINT_URL')
    SQS_REGION = os.getenv('SQS_REGION')
    SQS_QUEUE_NAME = os.getenv('SQS_QUEUE_NAME')

    client = boto3.resource('sqs',
                    endpoint_url=SQS_ENDPOINT_URL,
                    region_name=SQS_REGION,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    use_ssl=False)
    try:
        queue = client.get_queue_by_name(QueueName=SQS_QUEUE_NAME)
    except Exception as e:
        queue = client.create_queue(QueueName=SQS_QUEUE_NAME)

    logger.info(' [*] Waiting for events. To exit press CTRL+C')

    def event_callback(q, method, properties, body):
        """
        This function will be called when a message is received from SQS.
        Then it passes the message to the handler.
        """
        try:
            message = json.loads(body)
            logger.info(f" [x] Received events: {message}")

            # Call the handler with the event and a fictitious context
            # Here we simulate an AWS Lambda context
            event = {"Records": [{"body": body}]}  # This would be the SQS event
            context = {}  # This could be an object with details of the Lambda execution
            handler(event, context)  # Call the handler

        except Exception as e:
            logger.error(f"Error processing message: {e}")
        finally:
            q.delete_messages(Entries=[{'Id': method.message_id, 'ReceiptHandle': method.receipt_handle}])

    while True:
        for message in queue.receive_messages():
            event_callback(queue, message, None, message.body)   

def lambda_handler(event, context):
    """
    This function will be used by AWS Lambda, taking the event from SQS
    """
    handler(event, context)


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "sqs":
            logger.info("Starting SQS consumer.")
            consume_from_sqs()
        else:
            logger.info("No SQS consumer running.")
    except KeyboardInterrupt:
        logger.info("Exiting consumer.")
        sys.exit(0)
