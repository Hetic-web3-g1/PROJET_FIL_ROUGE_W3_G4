import logging

from fastapi import FastAPI
from fastapi.testclient import TestClient

from main import app  # noqa: F401
from src.database.db_engine import engine
from src.middlewares.log_error import LogErrorMiddleware
from src.utils.log.models import log_table


class TestLogger:
    """
    Test that the log handler is working properly,
    and that the error middleware is logging unexpected errors
    """

    @classmethod
    def setup_class(cls):
        cls.app = FastAPI()
        cls.app.add_middleware(LogErrorMiddleware)
        cls.test_client = TestClient(cls.app)

    @classmethod
    def setup_method(cls):
        with engine.begin() as conn:
            conn.execute(log_table.delete())

    def test_info_logging(self):
        @self.app.get("/warning")
        def dummy_endpoint():
            logging.warning("This is a warning log")
            return {"hello": "world"}

        self.test_client.get("/warning")
        with engine.begin() as conn:
            logs = conn.execute(
                log_table.select().where(log_table.c.level == "WARNING")
            ).fetchall()
            for log in logs:
                print(log._mapping)
            assert len(logs) == 1
            assert logs[0].level == "WARNING"
            assert logs[0].message == "This is a warning log"

    def test_error_logging(self):
        @self.app.get("/error")
        def dummy_endpoint():
            raise ValueError("This is an error log")

        self.test_client.get("/error")
        with engine.begin() as conn:
            logs = conn.execute(
                log_table.select().where(log_table.c.level == "ERROR")
            ).fetchall()
            assert len(logs) == 1
            assert logs[0].level == "ERROR"
            assert "This is an error log" in logs[0].message
