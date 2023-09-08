from unittest.mock import patch

from src.database.db_engine import engine
from src.entities.authentification import service as auth_service
from src.entities.users import service as user_service
from src.tests.fixtures import create_academy_with_admin_user_fixture
from src.tests.helpers import client

BASE_URI = "/api/users"


class TestUser:
    @classmethod
    def setup_class(cls):
        (
            cls.academy,
            cls.user,
            cls.academy_roles,
        ) = create_academy_with_admin_user_fixture("Test Academy")
        cls.token = auth_service.generate_jwt_token(cls.user)

    def test_create_user(self):
        with patch(
            "src.entities.authentification.service.send_reset_password_email"
        ) as mock:
            resp = client.post(
                f"{BASE_URI}/academy/{self.academy.id}/user",
                json={
                    "academy_id": str(self.academy.id),
                    "first_name": "blabla",
                    "last_name": "blabla",
                    "email": "balbla@gmail.com",
                    "role_id": 1,
                },
                headers={
                    "Authorization": f"Bearer {self.token}",
                },
            )

            assert resp.status_code == 200

            with engine.begin() as conn:
                created_user = user_service.get_user_by_email(conn, "balbla@gmail.com")

            assert created_user is not None
            mock.assert_called_once()
