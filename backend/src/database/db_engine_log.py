from sqlalchemy import create_engine, MetaData
from sqlalchemy_utils import database_exists, create_database

from utils.env import settings

# Connection to database
engine_log = create_engine(
    settings.database_log_url,
    connect_args={"options": "-c timezone=utc"}
)

# Check existence of db, if not, create it
if not database_exists(engine_log.url):
    create_database(engine_log.url)

metadata_log = MetaData()