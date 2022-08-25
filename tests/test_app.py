import pytest
from todo_app import app
from dotenv import load_dotenv, find_dotenv
import mongomock

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client

class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data

# Stub replacement for requests.get(url)
def get_lists_stub(url, params):
    fake_response_data = [{
        'id': '123abc',
        'name': 'To Do',
        'cards': [{'id': '456', 'name': 'Test card', 'dateLastActivity': '2022-02-08T17:36:12.1345Z', 'desc': '', 'due': ''}]
    }]
    return StubResponse(fake_response_data)