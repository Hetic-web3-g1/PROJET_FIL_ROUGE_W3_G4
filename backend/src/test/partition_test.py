from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_partitions():
    response = client.get("/partition")
    assert response.status_code == 200
    assert response.json() is not None, f"Response: {response.text}"

def test_create_partition():
    partition_data = {
        "status": "created",
        "file_name": "test_file_name",
        "created_by": "12345648-1234-1234-1234-123456789123"
    }
    response = client.post("/partition", json=partition_data)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"

    # Set the generated partition ID for other functions to use
    global partition_id
    partition_id = response.json()["data"]["value"][0]

def test_get_partition_by_id():
    # Use the generated partition ID to fetch the partition
    response = client.get(f"/partition/{partition_id}")
    assert response.status_code == 200
    assert response.json() is not None, f"Response: {response.text}"

def test_update_partition():
    updated_partition_data = {
        "file_name": "updated_file_name",
        "updated_by": "12345648-1234-1234-1234-123456789123"
    }
    response = client.put(f"/partition/{partition_id}", json=updated_partition_data)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"

def test_delete_partition():
    response = client.delete(f"/partition/{partition_id}")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"