from sqlalchemy.engine import Connection

from src.database import db_srv
from .schemas import Academy, AcademyCreate
from .models import academy_table


def _parse_row(row):
    return Academy(**row._asdict())


def create_academy(conn: Connection, academy: AcademyCreate) -> Academy:
    created_academy = db_srv.create_object(conn, academy_table, academy.dict())
    return created_academy