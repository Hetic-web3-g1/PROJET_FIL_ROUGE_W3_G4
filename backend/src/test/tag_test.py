from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_tags():
    # Retrieve all tags
    response = client.get("/tag")
    assert response.status_code == 200
    assert response.json() is not None, f"Response: {response.text}"

def test_create_tag():
    tag_data = {
        "content": "Test tag"
    }
    response = client.post("/tag", json=tag_data)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"
    # Set the generated tag ID for other functions to use
    global tag_id
    tag_id = response.json()["data"]["value"][0]

def test_get_tag_by_id():
    # Use the generated tag ID to fetch the tag
    response = client.get(f"/tag/{tag_id}")
    assert response.status_code == 200
    assert response.json() is not None, f"Response: {response.text}"

def test_update_tag():
    updated_tag_data = {
        "content": "Updated test tag"
    }
    response = client.put(f"/tag/{tag_id}", json=updated_tag_data)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"

def test_delete_tag():
    response = client.delete(f"/tag/{tag_id}")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"