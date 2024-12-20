from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from libs.database import get_db
from api.schemas.tests_generator import FilterParams
from libs.services.tests_generator import TestsGeneratorService


class TestsGeneratorController:
    def __init__(self):
        self.router = APIRouter(prefix="/tests", tags=["Tests Generator"])
        self._setup_routes()
        self.service = TestsGeneratorService

    def _setup_routes(self):
        self.router.add_api_route("/", self.get_tests, methods=["GET"], description="Generate tests for user stories but not save them to database")

    def get_tests(self, filter_params: Annotated[FilterParams, Query()] , db: Session = Depends(get_db)):
        try:
            service = self.service(db)
            user_story_id = filter_params.user_story_id
            if user_story_id:
                print(f"Debug: Fetching tests for user_story_id: {user_story_id}")
                tests = service.get_tests_by_user_story_id(user_story_id)
            else:
                tests = service.get_tests()
            return tests
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
