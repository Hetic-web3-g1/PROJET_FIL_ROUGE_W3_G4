from fastapi import APIRouter
from typing import List, Union

from database.db_engine import engine
from schema.response import ResponseModel
from utils.route_function import check_id, route_response, get_route_response
from schema.video import Video, VideoCreate, VideoUpdate
from manager import video_manager

router = APIRouter(
    prefix="/video",
    tags=["Video"],
)

# Get all videos
@router.get("", response_model=Union[List[Video], None])
def get_all_videos():
    with engine.begin() as conn:
        response = list(video_manager.get_all_video(conn))
        return get_route_response(response, 200, 404, "No videos found")

# Get video by id
@router.get("/{video_id}", response_model=Union[Video, None])
def get_video_by_id(video_id: str):
    check_id(video_id)
    with engine.begin() as conn:
        response = video_manager.get_video_by_id(conn, video_id)
        return get_route_response(response, 200, 404, "Video not found")

# Create video
@router.post("", response_model=ResponseModel)
def create_video(video: VideoCreate):
    with engine.begin() as conn:
        response = video_manager.create_video(conn, video)
        return route_response(response, 200, 500)

# Update video
@router.put("/{video_id}", response_model=ResponseModel)
def update_video(video_id: str, video: VideoUpdate):
    check_id(video_id)
    with engine.begin() as conn:
        response = video_manager.update_video(conn, video_id, video)
        return route_response(response, 200, 500)

# Delete video
@router.delete("/{video_id}", response_model=ResponseModel)
def delete_video(video_id: str):
    check_id(video_id)
    with engine.begin() as conn:
        response = video_manager.delete_video(conn, video_id)
        return route_response(response, 200, 500)