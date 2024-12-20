from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from libs.database import get_db
from api.schemas.events import EventResponse, EventsPayload
from libs.services.events import EventsService


class EventsController:
    def __init__(self):
        self.router = APIRouter(prefix="/events", tags=["Events"])
        self._setup_routes()
        self.service = EventsService

    def _setup_routes(self):
        self.router.add_api_route("/{event_id}", self.get_event_by_id, methods=["GET"])
        self.router.add_api_route("/", self.create_events, methods=["POST"], description="Save events to database and enqueue them to be processed")
    
    def create_events(self, events: EventsPayload, db: Session = Depends(get_db)):
        try:
            service = self.service(db)
            service.create_events(events)
            return {"message": "Events received and stored successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_event_by_id(self, event_id: str, db: Session = Depends(get_db)):
        try:
            service = self.service(db)
            event = service.get_event_by_id(event_id)
            if not event:
                raise HTTPException(status_code=404, detail="Event not found")
            return EventResponse.model_validate(event)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
