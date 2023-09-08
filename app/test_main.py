from fastapi.testclient import TestClient
from .main import app
from .main import DeepshoreChatRequest
import time

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Deepshore Chatbot API"}

def test_read_root():
    ts = int(time.time())
    req = {"question": "Was ist k6.io?", "timestamp": ts}
    response = client.post("/chatbot", json=req)
    assert response.status_code == 200

    res_object = response.json()

    assert res_object['timestamp'] == ts
    assert res_object['origin'] == req
    assert res_object['error'] == None