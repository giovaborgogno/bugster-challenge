from sqlalchemy import Column, String, Integer, JSON, DateTime

from api.database import Base


class UserStory(Base):
    __tablename__ = 'user_stories'
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    title = Column(String, index=True)
    startTimestamp = Column(DateTime)
    endTimestamp = Column(DateTime)
    initialState = Column(JSON)
    actions = Column(JSON)
    networkRequests = Column(JSON)
    finalState = Column(JSON)
