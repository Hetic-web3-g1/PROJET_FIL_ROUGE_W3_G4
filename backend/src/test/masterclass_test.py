from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_masterclasses():
    response = client.get("/masterclass")
    assert response.status_code == 200
    assert response.json() is not None, f"Response: {response.text}"

def test_create_masterclass():
    masterclass_data = {
        "title": "Test Masterclass",
        "description": "Test Masterclass Description",
        "status": "created",
        "academy_id": "12345648-1234-1234-1234-123456789123",
        "created_by": "12345648-1234-1234-1234-123456789123"
    }
    response = client.post("/masterclass", json=masterclass_data)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"

    # Set the generated masterclass ID for other functions to use
    global masterclass_id
    masterclass_id = response.json()["data"]["value"][0]

def test_get_masterclass_by_id():
    # Use the generated masterclass ID to fetch the masterclass
    response = client.get(f"/masterclass/{masterclass_id}")
    assert response.status_code == 200
    assert response.json() is not None, f"Response: {response.text}"

def test_update_masterclass():
    masterclass_data = {
        "title": "Updated Test Masterclass",
        "description": "Updated Test Masterclass Description",
        "updated_by": "12345648-1234-1234-1234-123456789123"
    }
    response = client.put(f"/masterclass/{masterclass_id}", json=masterclass_data)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"

def test_delete_masterclass():
    response = client.delete(f"/masterclass/{masterclass_id}")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"