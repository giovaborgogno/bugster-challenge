from typing import List

from sqlalchemy.orm import Session

from api.models.user_stories import UserStory
from api.services import mocks

class UserStoriesService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_stories_by_session(self, session_id: str) -> List[UserStory]:
        return mocks.user_stories
        # return self.db.query(UserStory).filter(UserStory.session_id == session_id)

    def get_user_stories(self) -> List[UserStory]:
        return mocks.user_stories
        # return self.db.query(UserStory).all()
