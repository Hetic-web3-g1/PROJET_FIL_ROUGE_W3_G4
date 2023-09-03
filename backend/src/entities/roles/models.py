import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from src.database.db_engine import metadata

role_table = sa.Table(
    "role",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("name", sa.String(255), nullable=False),
    sa.Column("description", sa.Text, nullable=False),
    sa.Column("service_rights", JSONB, nullable=False),
    sa.Column("academy_id", sa.UUID(as_uuid=True), sa.ForeignKey("academy.id")),
)
