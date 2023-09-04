import logging

from src.database import service as db_service

from ...database.db_engine import engine
from ...utils.log.log_table import log_table
from ...utils.log.log_schema import LogCreate


class LogHandler(logging.Handler):
    def emit(self, record):
        with engine.begin() as conn:
            log = LogCreate(level=record.levelname, message=record.msg)
            db_service.create_object(conn, log_table, log.dict())


# Create a custom formatter
format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Create handlers and set level of logs
logger = logging.getLogger("Log")
logger.setLevel(logging.DEBUG)

db_log = LogHandler()
console_log = logging.StreamHandler()
console_log.setFormatter(format)

# Add the handler to the logger
logger.addHandler(db_log)
logger.addHandler(console_log)
