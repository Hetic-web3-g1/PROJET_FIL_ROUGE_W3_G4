"""link_video_masterclass

Revision ID: 7a748bd6499e
Revises: e00d13d99399
Create Date: 2023-08-11 08:11:54.121882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7a748bd6499e"
down_revision = "e00d13d99399"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("video", sa.Column("masterclass_id", sa.UUID(), nullable=True))
    op.create_foreign_key(
        op.f("video_masterclass_id_fkey"),
        "video",
        "masterclass",
        ["masterclass_id"],
        ["id"],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f("video_masterclass_id_fkey"), "video", type_="foreignkey")
    op.drop_column("video", "masterclass_id")
    # ### end Alembic commands ###
