from sqlalchemy import Column, String, Integer, JSON, DateTime

from libs.database import Base


class UserStory(Base):
    __tablename__ = 'user_stories'
    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, index=True)
    title = Column(String, index=True)
    startTimestamp = Column(DateTime)
    endTimestamp = Column(DateTime)
    initialState = Column(JSON)
    actions = Column(JSON)
    networkRequests = Column(JSON)
    finalState = Column(JSON)
