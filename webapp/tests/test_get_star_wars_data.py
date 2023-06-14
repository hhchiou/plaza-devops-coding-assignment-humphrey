from fastapi.testclient import TestClient

from webapp.src.app import app

def test_get_star_wars_data():
    client = TestClient(app)
    response = client.get("/data")
    assert response.status_code == 200
    assert "name" in response.json()


def test_api_http_error():
    client = TestClient(app)
    response = client.get("/data?num=65535")
    assert response.status_code == 500
    assert response.json()["detail"] == "API Error"


def test_api_hello():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_api_top_people():
    client = TestClient(app)
    response = client.get("/top-people-by-bmi")
    assert response.status_code == 200
    assert len(response.json()) == 20
    assert "name" in response.json()[0]
