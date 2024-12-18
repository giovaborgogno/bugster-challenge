from typing import List

from sqlalchemy.orm import Session

from libs.models.user_stories import UserStory


class UserStoriesService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_stories_by_session(self, session_id: str) -> List[UserStory]:
        return self.db.query(UserStory).filter(UserStory.session_id == session_id).all()

    def get_user_stories(self) -> List[UserStory]:
        return self.db.query(UserStory).all()

    def get_user_stories_without_tests(self) -> List[UserStory]:
        return self.db.query(UserStory).filter(UserStory.hasTests==None).all()
    
    def get_user_story_by_id(self, user_story_id: str) -> UserStory:
        return self.db.query(UserStory).filter(UserStory.id==user_story_id).first()
