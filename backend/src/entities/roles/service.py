from uuid import UUID

from entities.roles.exceptions import RoleNotFound
from sqlalchemy.engine import Connection

from .models import role_table
from .schemas import Role, RoleCreate


def create_academy_role(conn: Connection, role: RoleCreate):
    stmt = role_table.insert().values(**role.dict()).returning(role_table)
    result = conn.execute(stmt).first()
    return Role(**result._asdict())


def get_academy_roles(conn: Connection, academy_id: UUID):
    stmt = role_table.select().where(role_table.c.academy_id == academy_id)
    result = conn.execute(stmt)
    return (Role(**role) for role in result.mappings())


def get_role_by_id(conn: Connection, role_id: int):
    stmt = role_table.select().where(role_table.c.id == role_id)
    result = conn.execute(stmt).first()
    if result:
        return Role(**result._asdict())
    else:
        raise RoleNotFound
