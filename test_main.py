from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

users = [
    {"id": 1, "admin": "Admin"},
    {"id": 2, "user1": "User1"},
    {"id": 3, "user2": "User2"}
]


def test_all_users():
    resp = client.get('/users')
    assert resp.status_code == 200
    assert resp.json() == {
        "users": users
    }


def test_user_id():
    resp = client.get("/users/2")
    assert resp.status_code == 200
    assert resp.json() == {
        "user": {"id": 2, "user1": "User1"}
    }

def test_get_user_id_error():
    resp = client.get("/users/100")
    assert resp.status_code == 400
    assert resp.json() == {
        "detail": f"User with id 100 is not found"
    }


def test_create_user():
    user_id = 4
    title = "User3"
    resp = client.post(f"/users/{user_id}",
                       params={"title": title}
                       )
    assert resp.status_code == 201
    assert resp.json() == {
        "new user": {"id": user_id, "title": title}
    }


def test_delete_user():
    resp = client.delete(f"/users/3")
    assert resp.status_code == 204

