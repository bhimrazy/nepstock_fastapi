from fastapi.testclient import TestClient
from nepstock_fastapi import main

client = TestClient(main.app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_nepstock_api_endpoint():
    response = client.get("/api/nepstock")
    assert response.status_code == 200
    
