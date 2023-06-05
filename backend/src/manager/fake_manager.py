from sqlalchemy.engine import Connection

from database import db_srv
from schema.user import UserCreate
from schema.academy import AcademyCreate

def create_fixed_user(conn: Connection, user: UserCreate):
    try:
        result = db_srv.create_object(conn, 'user', user, object_id="12345648-1234-1234-1234-123456789123")
        return {"status": "success", "message": "User created successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
def create_fixed_academy(conn: Connection, academy: AcademyCreate):
    try:
        result = db_srv.create_object(conn, 'academy', academy, object_id="12345648-1234-1234-1234-123456789123")
        return {"status": "success", "message": "Academy created successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}