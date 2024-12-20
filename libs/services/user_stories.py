from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from libs.models.events import Event
from libs.models.user_stories import UserStory
from libs.services.events import EventsService


class UserStoriesService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_stories_by_session(self, session_id: str) -> List[UserStory]:
        return self.db.query(UserStory).filter(UserStory.session_id == session_id).all()

    def get_user_stories(self) -> List[UserStory]:
        return self.db.query(UserStory).all()

    def get_user_stories_without_tests(self) -> List[UserStory]:
        return self.db.query(UserStory).filter(UserStory.hasTests==False).all()
    
    def get_user_story_by_id(self, user_story_id: str) -> UserStory:
        return self.db.query(UserStory).filter(UserStory.id==user_story_id).first()

    def create_user_story(self, user_story: UserStory) -> UserStory:
        self.db.add(user_story)
        self.db.commit()
        self.db.refresh(user_story)
        return user_story

    def generate_user_story(self, events: List[Event]) -> UserStory:
        user_story_id = f"us-{int(datetime.now().timestamp())}"
        
        start_timestamp = events[0].timestamp
        end_timestamp = events[-1].timestamp
        
        user_story = UserStory(
            id= user_story_id,
            session_id= events[0].properties['session_id'],
            title= "User Journey", 
            startTimestamp= start_timestamp,
            endTimestamp= end_timestamp,
            initialState= {
                "url": events[0].properties['current_url']
            },
            actions= [],
            networkRequests= [],  
            finalState= {
                "url": events[-1].properties['current_url']
            },
            hasTests= False
        )
        
        for event in events:
            action_type = event.properties['eventType']
            attributes = event.properties['elementAttributes']
            if action_type == "click" and attributes.get('href'):
                user_story.actions.append({
                    "type": "navigation",
                    "url": attributes.get('href'),
                })
            elif action_type == "click" and attributes.get('class'):
                user_story.actions.append({
                    "type": "click",
                    "target": attributes.get('class'),
                })
            elif action_type == "input":
                user_story.actions.append({
                    "type": "input",
                    "target": attributes.get('class'),
                    "value": event.properties['elementText']
                })
        
        return user_story

    def generate_user_stories(self, journey_id) -> List[UserStory]:
        grouped_events = EventsService(self.db).get_events_grouped_by_journey_id(journey_id)
        user_stories = []

        for _, events in grouped_events.items():
            user_story = self.generate_user_story(events)
            user_stories.append(user_story)
        return user_stories
