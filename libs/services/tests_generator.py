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
        test_code += "\n"
        
        return test_code 

    def _convert_user_story_to_test(self, user_story: UserStory) -> dict:
        test_name = f"test-{user_story.id}" 
        actions = user_story.actions
        
        test_steps = []
        assertions = []
        
        for action in actions:
            action_type = action.get('type')
            
            # I think the key to generate good tests is the good processesing of the user stories
            # so here we could add more logic, like locate by text, by class, by id, etc instead of just by page.locator()
            # I chose to use a map to avoid a long if-elif-else block, so we can easily add more action types and this way has direct access to the action
            action_map = {
                'input': lambda action: f'page.locator("{action.get("target")}").fill("{action.get("value")}")',
                'click': lambda action: f'page.locator("{action.get("target")}").click()',
                'navigation': lambda action: f'page.goto("{action.get("url")}")',
                # We can add more action types here
            }
            
            if action_type in action_map:
                test_steps.append(action_map[action_type](action))
            
        # I think we can use the finalState to generate the assertions, but we can also add more logic here
        if user_story.finalState:
            final_url = user_story.finalState.get('url')
            if final_url:
                assertions.append(f'expect(page.url()).to_be("{final_url}")')
            
           # we can add more assertions here
         
        test_code = self._generate_test_code(test_name, test_steps, assertions)

        # This function just generates the test data but doesn't save it in the database
        # so the user can review and modify the tests before saving them
        # We should use a Test model here
        return {"name": test_name, "story": user_story.id, "steps": test_steps, "assertions": assertions, "code": test_code} 

    def _generate_tests(self, user_stories: List[UserStory]) -> List[str]:
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
        # if user_story.hasTests:
        #     return user_story.tests
        return self._generate_tests([user_story])
