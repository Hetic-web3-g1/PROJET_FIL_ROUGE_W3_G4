from sqlalchemy.engine import Connection
from sqlalchemy import select
from typing import Union, Generator

from src.database import db_srv
from src.schema.video import Video, VideoCreate
from src.database.tables.video import video_table

def get_all_video(conn: Connection) -> Generator[Video, None, None]:
    result = conn.execute(select(video_table))
    if result is None:
        return
    else:
        for video_row in result:
            video_dict = video_row._asdict()
            yield Video(**video_dict)

def get_video_by_id(conn: Connection, video_id: str) -> Union[Video, None]:
    result = conn.execute(select(video_table).where(video_table.c.id == video_id))
    video_row = result.fetchone()
    if video_row is None:
        return None
    else:
        video_dict = video_row._asdict()
        return Video(**video_dict)

def create_video(conn: Connection, video: VideoCreate):
    try:
        result = db_srv.create_object(conn, video_table, video)
        return {"status": "success", "message": "Video created successfully", "value": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def update_video(conn: Connection, video_id: str, video: Video):
    try:
        filtered_video = {k: v for k, v in video.dict().items() if v is not None}
        result = db_srv.update_object(conn, 'video', video_id, filtered_video)
        return {"status": "success", "message": "Video updated successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def delete_video(conn: Connection, video_id: str):
    try:
        result = db_srv.delete_object(conn, 'video', video_id)
        return {"status": "success", "message": "Video deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}