from pydantic import BaseModel, Field, AliasChoices
from typing import List, Dict, Any

class EventProperties(BaseModel):
    distinct_id: str
    session_id: str
    journey_id: str
    current_url: str = Field(..., validation_alias=AliasChoices('$current_url','current_url') , serialization_alias='$current_url')
    host: str = Field(..., validation_alias=AliasChoices('$host','host') , serialization_alias='$host')
    pathname: str = Field(..., validation_alias=AliasChoices('$pathname','pathname') , serialization_alias='$pathname')
    browser: str = Field(..., validation_alias=AliasChoices('$browser','browser') , serialization_alias='$browser')
    device: str = Field(..., validation_alias=AliasChoices('$device','device') , serialization_alias='$device')
    screen_height: int = Field(..., validation_alias=AliasChoices('$screen_height','screen_height') , serialization_alias='$screen_height')
    screen_width: int = Field(..., validation_alias=AliasChoices('$screen_width','screen_width') , serialization_alias='$screen_width')
    eventType: str
    elementType: str
    elementText: str
    elementAttributes: Dict[str, Any]
    timestamp: str
    x: int
    y: int
    mouseButton: int
    ctrlKey: bool
    shiftKey: bool
    altKey: bool
    metaKey: bool

class Event(BaseModel):
    event: str
    properties: EventProperties
    timestamp: str

class EventsPayload(BaseModel):
    events: List[Event]

class EventResponse(Event):
    id: int

    class Config:
        populate_by_name = True
        from_attributes = True
