from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_work_analysis():
    response = client.get("/work_analysis")
    assert response.status_code == 200
    assert response.json() is not None, f"Response: {response.text}"

def test_create_work_analysis():
    work_analysis_data = {
        "name": "Test Work Analysis"
    }
    response = client.post("/work_analysis", json=work_analysis_data)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"

    # Set the generated work_analysis ID for other functions to use
    global work_analysis_id
    work_analysis_id = response.json()["data"]["value"][0]

def test_get_work_analysis_by_id():
    # Use the generated work_analysis ID to fetch the work_analysis
    response = client.get(f"/work_analysis/{work_analysis_id}")
    assert response.status_code == 200
    assert response.json() is not None, f"Response: {response.text}"

def test_update_work_analysis():
    updated_work_analysis_data = {
        "about": "Updated Test Work Analysis",
        "updated_by": "12345648-1234-1234-1234-123456789123"
    }
    response = client.put(f"/work_analysis/{work_analysis_id}", json=updated_work_analysis_data)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"

def test_delete_work_analysis():
    response = client.delete(f"/work_analysis/{work_analysis_id}")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"