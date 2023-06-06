from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_comments():
    response = client.get("/comment")
    assert response.status_code == 200
    assert response.json() is not None, f"Response: {response.text}"

def test_create_comment():
    comment_data = {
        "content": "Test comment",
        "created_by": "12345648-1234-1234-1234-123456789123"
    }
    response = client.post("/comment", json=comment_data)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"

    # Set the generated comment ID for other functions to use
    global comment_id
    comment_id = response.json()["data"]["value"][0]

def test_get_comment_by_id():
    # Use the generated comment ID to fetch the comment
    response = client.get(f"/comment/{comment_id}")
    assert response.status_code == 200
    assert response.json() is not None, f"Response: {response.text}"

def test_update_comment():
    updated_comment_data = {
        "content": "Updated test comment",
        "updated_by": "12345648-1234-1234-1234-123456789123"
    }
    response = client.put(f"/comment/{comment_id}", json=updated_comment_data)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"

def test_delete_comment():
    response = client.delete(f"/comment/{comment_id}")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"