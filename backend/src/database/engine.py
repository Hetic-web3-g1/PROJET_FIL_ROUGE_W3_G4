from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine.url import make_url

from config import settings
from src.utils.log.log_manager import log

make_url(settings.postgres_url)

# Connection to postgres
engine = create_engine(
    settings.postgres_url, connect_args={"options": "-c timezone=utc"}
)

metadata = MetaData()
