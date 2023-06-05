from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_biographies():
    response = client.get("/biography")
    assert response.status_code == 200
    assert response.json() is not None, f"Response: {response.text}"

def test_create_biography():
    biography_data = {
        "first_name": "John",
        "last_name": "Doe",
        "instrument": ["Guitar"],
        "nationality": "American",
        "website": "https://www.johndoe.com",
        "award": ["Grammy"],
        "content": "John Doe is a famous guitarist.",
        "type": "Composer",
        "status": "Created",
        "created_by": "12345648-1234-1234-1234-123456789123"
    }
    response = client.post("/biography", json=biography_data)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"

    # Set the generated biography ID for other functions to use
    global biography_id
    biography_id = response.json()["data"]["value"][0]

def test_get_biography_by_id():
    # Use the generated biography ID to fetch the biography
    response = client.get(f"/biography/{biography_id}")
    assert response.status_code == 200
    assert response.json() is not None, f"Response: {response.text}"

def test_update_biography():
    updated_biography_data = {
        "first_name": "John",
        "last_name": "Smith",
        "content": "John Smith is a famous guitarist.",
        "updated_by": "12345648-1234-1234-1234-123456789123"
    }
    response = client.put(f"/biography/{biography_id}", json=updated_biography_data)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"

def test_delete_biography():
    response = client.delete(f"/biography/{biography_id}")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"