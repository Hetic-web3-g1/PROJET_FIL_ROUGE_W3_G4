from unittest.mock import patch

from src.database.db_engine import engine
from src.entities.users import service as user_service
from src.tests.fixtures import create_academy_fixture, create_admin_user_fixture
from src.tests.helpers import client

BASE_URI = "/users"


class TestUser:
    @classmethod
    def setup_class(cls):
        cls.academy = create_academy_fixture("Test Academy")
        cls.admin_user, cls.token = create_admin_user_fixture(cls.academy.id)

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
