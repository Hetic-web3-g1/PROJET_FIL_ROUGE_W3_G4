"""add secondary role to user, rename masterclass_user role to masterclass_role

Revision ID: ef905a5ecf6f
Revises: 2335c7d393fc
Create Date: 2023-07-11 10:55:26.052815

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef905a5ecf6f'
down_revision = '2335c7d393fc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_tag',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_unique_constraint(None, 'masterclass', ['id'])
    op.add_column('masterclass_user', sa.Column('masterclass_role', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'masterclass_user', ['id'])
    op.drop_column('masterclass_user', 'role')
    op.add_column('user', sa.Column('primary_role', sa.String(), nullable=False))
    op.add_column('user', sa.Column('secondary_role', sa.ARRAY(sa.String()), nullable=True))
    op.drop_column('user', 'role')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('role', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('user', 'secondary_role')
    op.drop_column('user', 'primary_role')
    op.add_column('masterclass_user', sa.Column('role', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'masterclass_user', type_='unique')
    op.drop_column('masterclass_user', 'masterclass_role')
    op.drop_constraint(None, 'masterclass', type_='unique')
    op.drop_table('user_tag')
    # ### end Alembic commands ###
