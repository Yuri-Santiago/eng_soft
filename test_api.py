import pytest
from app import app, db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def test_create_student(client):
    response = client.post("/students", json={
        "name": "Alice", "age": 17, "course": "Math"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Alice"
    assert data["age"] == 17
    assert data["course"] == "Math"

def test_get_all_students(client):
    client.post("/students", json={
        "name": "Bob", "age": 18, "course": "Physics"
    })
    response = client.get("/students")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "Bob"

def test_get_single_student(client):
    res = client.post("/students", json={
        "name": "Carol", "age": 19, "course": "Biology"
    })
    student_id = res.get_json()["id"]
    response = client.get(f"/students/{student_id}")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Carol"

def test_update_student(client):
    res = client.post("/students", json={
        "name": "Dan", "age": 20, "course": "History"
    })
    student_id = res.get_json()["id"]
    response = client.put(f"/students/{student_id}", json={
        "course": "Geography"
    })
    assert response.status_code == 200
    assert response.get_json()["course"] == "Geography"

def test_delete_student(client):
    res = client.post("/students", json={
        "name": "Eve", "age": 21, "course": "Philosophy"
    })
    student_id = res.get_json()["id"]
    delete_res = client.delete(f"/students/{student_id}")
    assert delete_res.status_code == 204
    get_res = client.get(f"/students/{student_id}")
    assert get_res.status_code == 404
