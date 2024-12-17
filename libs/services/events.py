import json

import pika
from sqlalchemy.orm import Session

from libs.models.events import Event

class EventsService:
    def __init__(self, db: Session):
        self.db = db
        self.rabbitmq_host = "localhost"

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
                self.publish_to_rabbitmq(json.dumps({"journey_id": journey_id}))
        except Exception as e:
            self.db.rollback()
            raise e

    def publish_to_rabbitmq(self, message) -> None:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host))
            channel = connection.channel()

            channel.exchange_declare(exchange='event_exchange', exchange_type='fanout')

            channel.basic_publish(exchange='event_exchange', routing_key='', body=message)

            print(" [x] Sent events to RabbitMQ")

            connection.close()
        except Exception as e:
            print(f"Error sending message to RabbitMQ: {e}")
        
    def get_event_by_id(self, event_id: str) -> Event:
        return self.db.query(Event).filter(Event.id == event_id).first()