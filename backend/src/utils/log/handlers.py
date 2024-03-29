import logging
import traceback

from src.database import service as db_service
from src.database.db_engine import engine
from src.utils.log.models import log_table
from src.utils.log.schemas import LogCreate


class LogHandler(logging.Handler):
    def emit(self, record):
        message = record.getMessage()

        if record.exc_info:  # if exception, get the full traceback
            message = traceback.format_exc(chain=False)

        with engine.begin() as conn:
            log = LogCreate(level=record.levelname, message=message)
            db_service.create_object(conn, log_table, log.dict())


def setup_logger():
    console_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_log = logging.StreamHandler()
    console_log.setFormatter(console_format)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logger.addHandler(LogHandler())
    logger.addHandler(console_log)
