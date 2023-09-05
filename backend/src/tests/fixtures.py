from typing import TypedDict

from scripts.create_academy import DEFAULT_ACADEMY_ROLES
from src.database.db_engine import engine
from src.entities.academies import service as academy_service
from src.entities.academies.schemas import Academy, AcademyCreate
from src.entities.roles import service as role_service
from src.entities.roles.schemas import Role, RoleCreate
from src.entities.users import service as user_service
from src.entities.users.schemas import User, UserCreate


class GeneratedRoles(TypedDict):
    admin_role: Role
    writer_role: Role
    film_crew_role: Role


def create_academy_with_admin_user_fixture(
    academy_name: str, user_email: str = "test@gmail.com"
) -> tuple[Academy, User, GeneratedRoles]:
    with engine.begin() as conn:
        academy = academy_service.create_academy(conn, AcademyCreate(name=academy_name))

        admin_role = role_service.create_academy_role(
            conn, RoleCreate(**DEFAULT_ACADEMY_ROLES["Admin"], academy_id=academy.id)
        )
        writer_role = role_service.create_academy_role(
            conn, RoleCreate(**DEFAULT_ACADEMY_ROLES["Writer"], academy_id=academy.id)
        )
        film_crew_role = role_service.create_academy_role(
            conn,
            RoleCreate(
                **DEFAULT_ACADEMY_ROLES["Film crew member"], academy_id=academy.id
            ),
        )

        user = user_service.create_user(
            conn,
            UserCreate(
                academy_id=academy.id,
                first_name="Admin User",
                last_name="Admin User",
                email=user_email,
                role_id=admin_role.id,
            ),
        )

        return (
            academy,
            user,
            GeneratedRoles(
                admin_role=admin_role,
                writer_role=writer_role,
                film_crew_role=film_crew_role,
            ),
        )
