from typing import List

from sqlalchemy.orm import Session

from libs.models.user_stories import UserStory
from libs.services.user_stories import UserStoriesService


class TestsGeneratorService:
    def __init__(self, db: Session):
        self.db = db

    def _generate_test_code(self, name, steps, assertions) -> str:
        test_code = f"def {name}(page):\n"
        test_code += "    # Test steps\n    "
        test_code += "\n    ".join(steps)
        test_code += "\n\n    # Assertions\n    "
        test_code += "\n    ".join(assertions)
        
        return test_code 

    def _convert_user_story_to_test(self, user_story: UserStory) -> str:
        test_name = f"test_{user_story.id}" 
        actions = user_story.actions
        
        test_steps = []
        assertions = []
        
        for action in actions:
            action_type = action.get('type')
            target = action.get('target')
            
            if action_type == 'input':
                value = action.get('value')
                test_steps.append(f'page.locator("{target}").fill("{value}")')
            
            elif action_type == 'click':
                test_steps.append(f'page.locator("{target}").click()')
            
            elif action_type == 'navigation':
                url = action.get('url')
                test_steps.append(f'page.goto("{url}")')
            
            # We can add more action types here
 
        if user_story.finalState:
            final_url = user_story.finalState.get('url')
            if final_url:
                assertions.append(f'expect(page.url()).to_be("{final_url}")')
            
            # hardcoded assertion for displayName for now
            if 'displayName' in user_story.finalState:
                display_name = user_story.finalState['displayName']
                assertions.append(f'expect(page.locator("#display-name")).to_have_text("{display_name}")')
        test_code = self._generate_test_code(test_name, test_steps, assertions)
        # We should use a Test model here
        return {"name": test_name, "story": user_story.id, "steps": test_steps, "assertions": assertions, "code": test_code} 

    def _generate_tests(self, user_stories: List[UserStory]) -> List[str]:
        # Aquí iría la lógica para generar los tests a partir de las user stories
        tests = []
        for story in user_stories:
            tests.append(self._convert_user_story_to_test(story))
        return tests
    
    def get_tests(self) -> List[str]:
        # For simplicity we are not saving the tests in the database
        # existing_tests = self.db.query(Tests).all()
        existing_tests = []
        
        new_user_stories = UserStoriesService(self.db).get_user_stories_without_tests()
        
        if new_user_stories:
            existing_tests.extend(self._generate_tests(new_user_stories))
        
        return existing_tests 

    def get_tests_by_user_story_id(self, user_story_id):
        user_story = UserStoriesService(self.db).get_user_story_by_id(user_story_id)
        print(f"Debug: Story: {user_story}")
        if not user_story:
            return []
        # For simplicity we are not saving the tests in the database
        # if user_story.has_tests:
        #     return user_story.tests
        return self._generate_tests([user_story])
