from sqlalchemy import create_engine, MetaData

from config import settings

# Connection to postgres
engine = create_engine(
    settings.postgres_url, connect_args={"options": "-c timezone=utc"}
)

metadata = MetaData()
