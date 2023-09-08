from src.database.db_engine import engine
from src.entities.academies import service as academy_service
from src.entities.academies.schemas import AcademyCreate
from src.entities.roles import service as role_service
from src.entities.roles.schemas import Right, Role, RoleCreate, Service
from src.entities.users import service as user_service
from src.entities.users.schemas import UserCreate

ORGANIZATION_NAME = "Saline academy"

# Suggestions of roles for a new academy
DEFAULT_ACADEMY_ROLES = {
    "Admin": {
        "name": "Admin",
        "description": "Access to all services, including user management",
        "service_rights": {
            Service.USER_MANAGEMENT: Right.EDITOR,
            Service.MASTERCLASS: Right.EDITOR,
            Service.BIOGRAPHY: Right.EDITOR,
        },
    },
    "Writer": {
        "name": "Writer",
        "description": "Can upload text documents",
        "service_rights": {
            Service.MASTERCLASS: Right.VIEWER,
            Service.BIOGRAPHY: Right.EDITOR,
        },
    },
    "Film crew member": {
        "name": "Film crew member",
        "description": "Can be assigned to a masterclass to upload videos",
        "service_rights": {
            Service.MASTERCLASS: Right.VIEWER,
            Service.BIOGRAPHY: Right.VIEWER,
        },
    },
}


def main():
    academy = AcademyCreate(name=ORGANIZATION_NAME)
    with engine.begin() as conn:
        academy = academy_service.create_academy(conn, academy)
        created_roles: list[Role] = []
        for role in DEFAULT_ACADEMY_ROLES.values():
            created_role = role_service.create_academy_role(
                conn, RoleCreate(**role, academy_id=academy.id)
            )
            created_roles.append(created_role)

        admin_role = next((role for role in created_roles if role.name == "Admin"))

        user_service.create_user(
            conn,
            UserCreate(
                academy_id=academy.id,
                email="test@gmail.com",
                first_name="Test",
                last_name="Test",
                role_id=admin_role.id,
            ),
            password="test",
        )


if __name__ == "__main__":
    main()
