from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_users():
    response = client.get("/user")
    assert response.status_code == 200
    assert response.json() is not None, f"Response: {response.text}"

def test_create_user():
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "academy_id": "12345648-1234-1234-1234-123456789123"
    }
    response = client.post("/user", json=user_data)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"

    # Set the generated user ID for other functions to use
    global user_id
    user_id = response.json()["data"]["value"][0]

def test_get_user_by_id():
    # Use the generated user ID to fetch the user
    response = client.get(f"/user/{user_id}")
    assert response.status_code == 200
    assert response.json() is not None, f"Response: {response.text}"

def test_update_user():
    updated_user_data = {
        "first_name": "John",
        "last_name": "Smith",
        "email": "john.smith@example.com",
        "password": "newpassword",
        "updated_by": "12345648-1234-1234-1234-123456789123"
    }
    response = client.put(f"/user/{user_id}", json=updated_user_data)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"

def test_delete_user():
    response = client.delete(f"/user/{user_id}")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"