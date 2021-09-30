from fastapi.testclient import TestClient
from app import main

client = TestClient(main.app)


def test_read_main():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_nepstock_api_endpoint():
    """Test API endpoint"""
    response = client.get("/api/nepstock")
    assert response.status_code == 200
