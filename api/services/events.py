from sqlalchemy.orm import Session
from api.models.events import Event

class EventsService:
    def __init__(self, db: Session):
        self.db = db

    def create_events(self, events) -> None:
        try:
            for event_data in events.events:
                event = Event(
                    event=event_data.event,
                    properties=event_data.properties.dict(),
                    timestamp=event_data.timestamp
                )
                self.db.add(event)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        
    def get_event_by_id(self, event_id: str) -> Event:
        return self.db.query(Event).filter(Event.id == event_id).first()