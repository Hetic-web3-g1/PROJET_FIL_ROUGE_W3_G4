from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_academies():
    response = client.get("/academy")
    assert response.status_code == 200
    assert response.json() is not None, f"Response: {response.text}"

def test_create_academy():
    academy_data = {
        "name": "Test Academy"
    }
    response = client.post("/academy", json=academy_data)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"

    # Set the generated academy ID for other functions to use
    global academy_id
    academy_id = response.json()["data"]["value"][0]

def test_get_academy_by_id():
    # Use the generated academy ID to fetch the academy
    response = client.get(f"/academy/{academy_id}")
    assert response.status_code == 200
    assert response.json() is not None, f"Response: {response.text}"

def test_update_academy():
    updated_academy_data = {
        "name": "Updated Test Academy"
    }
    response = client.put(f"/academy/{academy_id}", json=updated_academy_data)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"
    
def test_delete_academy():
    response = client.delete(f"/academy/{academy_id}")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"