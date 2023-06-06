from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_videos():
    response = client.get("/video")
    assert response.status_code == 200
    assert response.json() is not None, f"Response: {response.text}"

def test_create_video():
    video_data = {
        "version": 1.0,
        "title": "Test Video",
        "duration": 60,
        "status": "created",
        "file_name": "test_video.mp4",
        "created_by": "12345648-1234-1234-1234-123456789123"
    }
    response = client.post("/video", json=video_data)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"

    # Set the generated video ID for other functions to use
    global video_id
    video_id = response.json()["data"]["value"][0]

def test_get_video_by_id():
    # Use the generated video ID to fetch the video
    response = client.get(f"/video/{video_id}")
    assert response.status_code == 200
    assert response.json() is not None, f"Response: {response.text}"

def test_update_video():
    updated_video_data = {
        "version": 1.1,
        "title": "Updated Test Video",
        "status": "created",
        "updated_by": "12345648-1234-1234-1234-123456789123"
    }
    response = client.put(f"/video/{video_id}", json=updated_video_data)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"

def test_delete_video():
    response = client.delete(f"/video/{video_id}")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success", f"Response: {response.text}"