import json
import os
from typing import List

import boto3
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from libs.models.events import Event
from datetime import datetime


class EventsService:
    def __init__(self, db: Session):
        self.db = db

    def create_events(self, events) -> None:
        try:
            journey_ids = set()
            for event_data in events.events:
                event = Event(
                    event=event_data.event,
                    properties=event_data.properties.dict(),
                    timestamp=event_data.timestamp
                )
                self.db.add(event)
                journey_ids.add(event_data.properties.journey_id)
            self.db.commit()
            for journey_id in journey_ids:
                self.publish_to_sqs(json.dumps({"journey_id": journey_id}))
        except Exception as e:
            self.db.rollback()
            raise e
        
    def publish_to_sqs(self, message) -> None:
        try:
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

            queue.send_message(MessageBody=message)

            print(" [x] Sent events to SQS")
        except Exception as e:
            print(f"Error sending message to SQS: {e}")
        
    def get_event_by_id(self, event_id: str) -> Event:
        return self.db.query(Event).filter(Event.id == event_id).first()

    def get_events_by_journey_id(self, journey_id: str = None) -> List[Event]:
        if journey_id:
            # For some reason this query filtering is not working, so I'm filtering manually for simplicity
            # events = self.db.query(Event).filter(Event.properties['journey_id'] == journey_id).all()
            events = self.db.query(Event).all()
            events = [event for event in events if event.properties['journey_id'] == journey_id]
        else:
            events = self.db.query(Event).all()
        events.sort(key=lambda event: datetime.strptime(event.timestamp, '%Y-%m-%dT%H:%M:%S.%fZ'))
        return events