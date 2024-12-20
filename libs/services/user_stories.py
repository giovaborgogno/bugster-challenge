from datetime import datetime
from typing import List

from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from libs.models.events import Event
from libs.models.user_stories import UserStory


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
        """
        Generate a user story from a list of events but without saving it
        """
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

        def get_target(attributes):
            class_list = attributes.get('class', '').split()
            return attributes.get('id') or f'.{".".join([f"{cls}" for cls in class_list])}'
        
        # I think this is the key to get good tests, we need to identify correctly the actions
        # for this example I'm just considering click and input events, and the target is the id or class of the element
        # but we should consider more attributes to identify the target. So in playwright we can use locators by id, class, text, attributes etc.
        for event in events:
            action_type = event.properties['eventType']
            attributes = event.properties['elementAttributes']
            if action_type == "click":
                if attributes.get('href'):
                    user_story.actions.append({
                        "type": "navigation", # Im assuming navigation is the same as click
                        "url": attributes['href'],
                    })
                else:
                    target = get_target(attributes)
                    if target:
                        user_story.actions.append({
                            "type": "click",
                            "target": target,
                        })
            elif action_type == "input":
                target = get_target(attributes)
                if target:
                    user_story.actions.append({
                        "type": "input",
                        "target": target,
                        "value": event.properties['elementText']
                    })
        
        return user_story

    def identify_common_patterns(self, user_story: UserStory) -> UserStory:
        """
        Identifies a common pattern for the user story and assigns a tag.
        """
        # existing_user_stories = self.get_user_stories()
        # For the sake of simplicity, we will use a hardcoded list of existing user stories
        existing_user_stories = [
            UserStory(actions=[
                {"type": "input", "target": "#email", "value": "jhon_doe@email.com"},
                {"type": "input", "target": "#password", "value": "password"},
                {"type": "click", "target": "#login-button"}
            ], tags=["login"]),
            
            UserStory(actions=[
                {"type": "navigate", "target": "/home"},
                {"type": "click", "target": "#search"},
                {"type": "input", "value": "product"}
            ], tags=["search"]),
        ]
        
        return PatternIdentifier().identify_patterns(user_story, existing_user_stories)


class PatternIdentifier:
    def __init__(self):
        self.vectorizer = CountVectorizer()

    def extract_actions(self, user_story: UserStory) -> str:
        """
        Extracts actions from a user story and formats them as a single string.
        """
        actions = []
        for action in user_story.actions:
            # We should consider more attributes for a more accurate pattern identification
            action_str = f"{action['type']}:{action.get('target', '')}:{action.get('value', '')}:{action.get('url', '')}"
            actions.append(action_str)
        return " ".join(actions)

    def identify_patterns(self, user_story, existing_user_stories) -> UserStory:
        # Get the vector for the existing user stories
        actions = [self.extract_actions(story) for story in existing_user_stories]
        tags = [story.tags for story in existing_user_stories]
        actions_vector = self.vectorizer.fit_transform(actions)
        
        # Get the vector for the new user story
        new_action_str = self.extract_actions(user_story)
        new_action_vector = self.vectorizer.transform([new_action_str])
        
        # Calculate cosine similarity between the new user story vector and existing user story vectors
        similarities = cosine_similarity(new_action_vector, actions_vector)
        
        # Set a similarity threshold (60% in this case)
        similarity_threshold = 0.6
        
        max_similarity = similarities.max()
        if max_similarity >= similarity_threshold:
            most_similar_index = similarities.argmax()
            user_story.tags = tags[most_similar_index]
        
        return user_story
