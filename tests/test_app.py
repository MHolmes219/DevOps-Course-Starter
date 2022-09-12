import pytest
from todo_app import app
from dotenv import load_dotenv, find_dotenv
import mongomock
import pymongo
import os

import mongomock
@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client


def test_index_page(client):

    collection = pymongo.MongoClient("mongodb://fakemongo.com")
    database = os.environ.get('DATABASE')

    card = {
        "_id": "6307641f3faf4947e58a5166",
        "name": "Test card",
        "dateLastActivity": mongomock.utcnow(),
        "desc": "Test Description",
        "due": "08/24/2022",
        "list": "To Do"
    }

    collection[database].cards.insert_one(card)

    response = client.get('/')

    assert response.status_code == 200
    assert 'Test card' in response.data.decode()
