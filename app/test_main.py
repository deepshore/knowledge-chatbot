from fastapi.testclient import TestClient
from .main import app
from .main import DeepshoreChatRequest
import time

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Deepshore Chatbot API"}

def test_post_chatbot():
    ts = int(time.time())
    req = {"question": "Was ist k6.io?", "timestamp": ts}
    response = client.post("/chatbot", json=req)
    assert response.status_code == 200

    res_object = response.json()

    print(res_object['related_articles'])

    assert res_object['related_articles'] == ['https://deepshore.de/knowledge/2023-05-08', 'https://deepshore.de/knowledge/2023-05-08']
    assert res_object['timestamp'] == ts
    assert res_object['origin'] == req
    assert res_object['error'] == None