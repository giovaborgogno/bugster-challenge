import uvicorn
from fastapi import APIRouter, FastAPI
from mangum import Mangum

from api.controllers.tests_generator import TestsGeneratorController
from api.controllers.user_stories import UserStoriesController
from libs.database import engine, Base
from api.controllers.events import EventsController


Base.metadata.create_all(bind=engine)

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
    title="Bugster Challenge API",
    version="v1",
    root_path=f"/api/v1"
)


main_router = APIRouter(tags=["Main"])

@main_router.get("/")
async def root():
    return {"message": "Hello World", "version": "v1"}

events_controller = EventsController()
stories_controller = UserStoriesController()
tests_generator_controller = TestsGeneratorController()

app.include_router(main_router)
app.include_router(events_controller.router)
app.include_router(stories_controller.router)
app.include_router(tests_generator_controller.router)

lambda_handler = Mangum(app, lifespan="off", api_gateway_base_path="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3100)
