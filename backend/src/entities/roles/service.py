from uuid import UUID

from sqlalchemy.engine import Connection

from .models import role_table
from .schemas import Role, RoleCreate


def create_academy_role(conn: Connection, roles: RoleCreate):
    stmt = role_table.insert().values(**roles.dict())
    result = conn.execute(stmt)
    return (Role(**role) for role in result.mappings())

def get_academy_roles(conn: Connection, academy_id: UUID):
    stmt = role_table.select().where(role_table.c.academy_id == academy_id)
    result = conn.execute(stmt)
    return (Role(**role) for role in result.mappings())