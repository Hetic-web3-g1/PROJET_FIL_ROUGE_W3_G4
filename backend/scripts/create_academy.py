from src.database.db_engine import engine
from src.entities.academies import service as academy_service
from src.entities.academies.schemas import AcademyCreate
from src.entities.roles import service as role_service
from src.entities.roles.schemas import Right, RoleCreate, Service

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
    }
}

def main():
    academy = AcademyCreate(name=ORGANIZATION_NAME)
    with engine.begin() as conn:
        academy = academy_service.create_academy(conn, academy)
        for role in DEFAULT_ACADEMY_ROLES.values():
            role_service.create_academy_role(conn, RoleCreate(**role, academy_id=academy.id))

if __name__ == "__main__":
    main()
