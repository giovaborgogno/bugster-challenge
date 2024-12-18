from pydantic import BaseModel, Field


class FilterParams(BaseModel):
    user_story_id: str = Field(None)
 