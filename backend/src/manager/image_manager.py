from sqlalchemy.engine import Connection
from sqlalchemy import select
from typing import Union, Generator

from src.database import db_srv
from src.schema.image import Image, ImageCreate
from src.database.tables.image import image_table

def get_all_image(conn: Connection) -> Generator[Image, None, None]:
    result = conn.execute(select(image_table))
    if result is None:
        return
    else:
        for image_row in result:
            image_dict = image_row._asdict()
            yield Image(**image_dict)

def get_image_by_id(conn: Connection, image_id: str) -> Union[Image, None]:
    result = conn.execute(select(image_table).where(image_table.c.id == image_id))
    image_row = result.fetchone()
    if image_row is None:
        return
    else:
        image_dict = image_row._asdict()
        return Image(**image_dict)

def create_image(conn: Connection, image: ImageCreate):
    try:
        result = db_srv.create_object(conn, image_table, image)
        return {"status": "success", "message": "Image created successfully", "value": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def update_image(conn: Connection, image_id: str, image: Image):
    try:
        # Filter out None values from the image object
        filtered_image = {k: v for k, v in image.dict().items() if v is not None}
        result = db_srv.update_object(conn, 'image', image_id, filtered_image)
        return {"status": "success", "message": "Image updated successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def delete_image(conn: Connection, image_id: str):
    try:
        result = db_srv.delete_object(conn, 'image', image_id)
        return {"status": "success", "message": "Image deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}