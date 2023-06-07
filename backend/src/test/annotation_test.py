from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_annotations():
    response = client.get("/annotation")
    assert response.status_code == 200
    assert response.json() is not None, f"Response: {response.text}"

def test_create_annotation():
    annotation_data = {
        "measure": "1",
        "content": "This is an annotation",
        "created_by": "12345648-1234-1234-1234-123456789123"
    }
    response = client.post("/annotation", json=annotation_data)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"

    # Set the generated annotation ID for other functions to use
    global annotation_id
    annotation_id = response.json()["data"]["value"][0]

def test_get_annotation_by_id():
    # Use the generated annotation ID to fetch the annotation
    response = client.get(f"/annotation/{annotation_id}")
    assert response.status_code == 200
    assert response.json() is not None, f"Response: {response.text}"

def test_update_annotation():
    updated_annotation_data = {
        "annotation": "This is an updated annotation",
        "updated_by": "12345648-1234-1234-1234-123456789123"
    }
    response = client.put(f"/annotation/{annotation_id}", json=updated_annotation_data)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"

def test_delete_annotation():
    response = client.delete(f"/annotation/{annotation_id}")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"