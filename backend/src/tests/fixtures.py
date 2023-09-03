from uuid import UUID

from src.database.db_engine import engine
from src.entities.academies import service as academy_service
from src.entities.academies.schemas import AcademyCreate
from src.entities.authentification import service as auth_service
from src.entities.users import service as user_service
from src.entities.users.schemas import UserCreate


def create_academy_fixture(name: str):
    with engine.begin() as conn:
        return academy_service.create_academy(conn, AcademyCreate(name=name))


def create_admin_user_fixture(academy_id: UUID):
    with engine.begin() as conn:
        user = UserCreate(
            academy_id=academy_id,
            first_name="Admin User",
            last_name="Admin User",
            email="test@gmail.com",
        )
        created_user = user_service.create_user(conn, user, password="test_password")

        return created_user, auth_service.generate_jwt_token(created_user)
