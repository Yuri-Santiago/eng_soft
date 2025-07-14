import pytest
from app import app, db
from os import environ

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DATABASE_URL', 'sqlite:///:memory:')

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.rollback()
        db.session.remove()
        db.drop_all()

def test_create_teacher(client):
    response = client.post("/teachers", json={
        "name": "Dr. Smith", "department": "Physics"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Dr. Smith"
    assert data["department"] == "Physics"

def test_get_all_teachers(client):
    client.post("/teachers", json={
        "name": "Dr. Jones", "department": "Chemistry"
    })
    response = client.get("/teachers")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "Dr. Jones"

def test_get_single_teacher(client):
    res = client.post("/teachers", json={
        "name": "Dr. Allen", "department": "Biology"
    })
    teacher_id = res.get_json()["id"]
    response = client.get(f"/teachers/{teacher_id}")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Dr. Allen"

def test_update_teacher(client):
    res = client.post("/teachers", json={
        "name": "Dr. Lee", "department": "Mathematics"
    })
    teacher_id = res.get_json()["id"]
    response = client.put(f"/teachers/{teacher_id}", json={
        "department": "Statistics"
    })
    assert response.status_code == 200
    assert response.get_json()["department"] == "Statistics"

def test_delete_teacher(client):
    res = client.post("/teachers", json={
        "name": "Dr. Kim", "department": "Philosophy"
    })
    teacher_id = res.get_json()["id"]
    delete_res = client.delete(f"/teachers/{teacher_id}")
    assert delete_res.status_code == 204
    get_res = client.get(f"/teachers/{teacher_id}")
    assert get_res.status_code == 404
