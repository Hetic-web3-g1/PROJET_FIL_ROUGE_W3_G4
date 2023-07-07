from sqlalchemy.engine import Connection
from sqlalchemy import select
from typing import Union, Generator

from src.database import db_srv
from src.users.schemas import User, UserCreate
from src.users.models import user_table

def get_all_user(conn: Connection) -> Generator[User, None, None]:
    result = conn.execute(select(user_table))
    if result is None:
        return None
    else:
        for user_row in result:
            user_dict = user_row._asdict()
            yield User(**user_dict)

def get_user_by_id(conn: Connection, user_id: str) -> Union[User, None]:
    result = conn.execute(select(user_table).where(user_table.c.id == user_id))
    user_row = result.fetchone()
    if user_row is None:
        return None
    else:
        user_dict = user_row._asdict()
        return User(**user_dict)

def create_user(conn: Connection, user: UserCreate):
    try:
        result = db_srv.create_object(conn, user_table, user)
        return {"status": "success", "message": "User created successfully", "value": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def update_user(conn: Connection, user_id: str, user: User):
    try:
        # Filter out None values from the user object
        filtered_user = {k: v for k, v in user.dict().items() if v is not None}
        result = db_srv.update_object(conn, 'user', user_id, filtered_user)
        return {"status": "success", "message": "User updated successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

    
def delete_user(conn: Connection, user_id: str):
    try:
        result = db_srv.delete_object(conn, 'user', user_id)
        return {"status": "success", "message": "User deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}