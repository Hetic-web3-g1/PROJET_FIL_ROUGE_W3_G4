from unittest import TestCase

from entities.users.schemas import UserCreate
from fastapi import HTTPException

from src.database.db_engine import engine
from src.entities.authentification import service as auth_service
from src.entities.authentification.dependencies import CustomSecurity
from src.entities.roles.schemas import Right, Service
from src.entities.users import service as user_service
from src.tests.fixtures import create_academy_with_admin_user_fixture


class TestAuthentitifcation(TestCase):
    @classmethod
    def setup_class(cls):
        (
            cls.academy,
            cls.user,
            cls.academy_roles,
        ) = create_academy_with_admin_user_fixture("Test Academy")
        cls.token = auth_service.generate_jwt_token(cls.user)

    def test_auth_invalid_token(self):
        auth_dependency = CustomSecurity({Service.BIOGRAPHY: Right.EDITOR})
        with self.assertRaises(HTTPException) as cm:
            auth_dependency(None, "invalid_token")

        assert cm.exception is not None
        assert cm.exception.status_code == 401

    def test_auth_valid_token_and_right(self):
        with engine.begin() as conn:
            writer_user = user_service.create_user(
                conn,
                UserCreate(
                    academy_id=self.academy.id,
                    first_name="TEST_USER",
                    last_name="",
                    email="test1@gmail.com",
                    role_id=self.academy_roles["writer_role"].id,
                ),
            )
        auth_dependency = CustomSecurity({Service.BIOGRAPHY: Right.EDITOR})
        user = auth_dependency(None, auth_service.generate_jwt_token(writer_user))

        assert user.email == "test1@gmail.com"

    def test_auth_valid_token_and_no_right(self):
        with engine.begin() as conn:
            film_crew_user = user_service.create_user(
                conn,
                UserCreate(
                    academy_id=self.academy.id,
                    first_name="TEST_USER",
                    last_name="",
                    email="test2@gmail.com",
                    role_id=self.academy_roles["film_crew_role"].id,
                ),
            )
        auth_dependency = CustomSecurity({Service.BIOGRAPHY: Right.EDITOR})

        with self.assertRaises(HTTPException) as cm:
            auth_dependency(None, auth_service.generate_jwt_token(film_crew_user))

        assert cm.exception is not None
        assert cm.exception.status_code == 403
