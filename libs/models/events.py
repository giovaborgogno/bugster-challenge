from sqlalchemy import Column, String, Integer, JSON

from libs.database import Base


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, index=True)
    event = Column(String, index=True)
    properties = Column(JSON)
    timestamp = Column(String, index=True)
