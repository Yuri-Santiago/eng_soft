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

def test_create_classroom(client):
    response = client.post("/classrooms", json={
        "name": "Turma A", "semester": "2025.1"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Turma A"
    assert data["semester"] == "2025.1"

def test_get_all_classrooms(client):
    client.post("/classrooms", json={"name": "Turma B", "semester": "2025.2"})
    response = client.get("/classrooms")
    assert response.status_code == 200
    assert len(response.get_json()) == 1

def test_get_single_classroom(client):
    res = client.post("/classrooms", json={"name": "Turma C", "semester": "2025.3"})
    classroom_id = res.get_json()["id"]
    response = client.get(f"/classrooms/{classroom_id}")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Turma C"

def test_update_classroom(client):
    res = client.post("/classrooms", json={"name": "Turma D", "semester": "2025.4"})
    classroom_id = res.get_json()["id"]
    response = client.put(f"/classrooms/{classroom_id}", json={"semester": "2025.5"})
    assert response.status_code == 200
    assert response.get_json()["semester"] == "2025.5"

def test_delete_classroom(client):
    res = client.post("/classrooms", json={"name": "Turma E", "semester": "2025.6"})
    classroom_id = res.get_json()["id"]
    response = client.delete(f"/classrooms/{classroom_id}")
    assert response.status_code == 204
    response = client.get(f"/classrooms/{classroom_id}")
    assert response.status_code == 404
