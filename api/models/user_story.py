from sqlalchemy import Column, String, Integer, JSON

from api.database import Base


class UserStory(Base):
    __tablename__ = 'user_stories'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    actions = Column(JSON)
