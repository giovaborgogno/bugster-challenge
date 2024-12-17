from pydantic import BaseModel, Field


class FilterParams(BaseModel):
    session_id: str = Field(None)
 