from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_images():
    response = client.get("/image")
    assert response.status_code == 200
    assert response.json() is not None, f"Response: {response.text}"

def test_create_image():
    image_data = {
        "title": "Test Image",
        "file_name": "test_image.jpg",
        "created_by": "12345648-1234-1234-1234-123456789123"
    }
    response = client.post("/image", json=image_data)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"

    # Set the generated image ID for other functions to use
    global image_id
    image_id = response.json()["data"]["value"][0]

def test_get_image_by_id():
    # Use the generated image ID to fetch the image
    response = client.get(f"/image/{image_id}")
    assert response.status_code == 200
    assert response.json() is not None, f"Response: {response.text}"

def test_update_image():
    updated_image_data = {
        "title": "Updated Image",
        "file_name": "updated_image.jpg",
        "updated_by": "12345648-1234-1234-1234-123456789123"
    }
    response = client.put(f"/image/{image_id}", json=updated_image_data)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"

def test_delete_image():
    response = client.delete(f"/image/{image_id}")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"