from unittest.mock import patch
from fastapi.testclient import TestClient

from api.main import app
from api.tests import mocks

client = TestClient(app)


@patch('libs.services.user_stories.UserStoriesService.get_user_stories')
def test_get_user_stories(mock_user_stories):
    mock_user_stories.return_value = mocks.user_stories
    response = client.get("/stories/")
    assert response.status_code == 200
    stories = response.json()
    assert stories == mocks.user_stories
    
@patch('libs.services.user_stories.UserStoriesService.get_user_stories_by_session')
def test_get_user_stories_by_session(mock_user_stories):
    mock_user_stories.return_value = mocks.user_stories
    session_id = "fcc95c16-28ae-4bc5-bead-cf052ab87cef"
    response = client.get(f"/stories?session_id={session_id}")
    assert response.status_code == 200
    stories = response.json()
    assert stories == mocks.user_stories
    mock_user_stories.assert_called_once_with(session_id)
