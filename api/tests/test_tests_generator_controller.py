from unittest.mock import patch
from fastapi.testclient import TestClient

from api.main import app
from api.tests import mocks
from libs.models.user_stories import UserStory

client = TestClient(app)


class TestTController:
    @patch('libs.services.user_stories.UserStoriesService.get_user_stories_without_tests')
    def test_get_tests(self, mock_user_stories):
        mock_user_stories.return_value = [UserStory(**story) for story in mocks.user_stories]
        response = client.get("/tests/")
        assert response.status_code == 200
        
    @patch('libs.services.user_stories.UserStoriesService.get_user_story_by_id')
    def test_get_tests_by_user_story_id(self, mock_user_stories):
        mock_user_stories.return_value = UserStory(**mocks.user_stories[0])
        user_story_dict = mocks.user_stories[0]
        mock_user_story = UserStory(**user_story_dict)
        mock_user_stories.return_value = mock_user_story
        user_story_id = "fcc95c16-28ae-4bc5-bead-cf052ab87cef"
        response = client.get(f"/tests?user_story_id={user_story_id}")
        assert response.status_code == 200
        mock_user_stories.assert_called_once_with(user_story_id)

        assert response.json()[0]["code"] == mocks.code
