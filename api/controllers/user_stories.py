from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from libs.database import get_db
from api.schemas.user_stories import FilterParams
from libs.services.user_stories import UserStoriesService


class UserStoriesController:
    def __init__(self):
        self.router = APIRouter(prefix="/stories", tags=["User Stories"])
        self._setup_routes()
        self.service = UserStoriesService

    def _setup_routes(self):
        self.router.add_api_route("/", self.get_user_stories, methods=["GET"])

    def get_user_stories(self, filter_params: Annotated[FilterParams, Query()] , db: Session = Depends(get_db)):
        try:
            service = self.service(db)
            session_id = filter_params.session_id
            if session_id:
                print(f"Debug: Fetching user stories for session_id: {session_id}")
                user_stories = service.get_user_stories_by_session(session_id)
            else:
                user_stories = service.get_user_stories()
            return user_stories
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
