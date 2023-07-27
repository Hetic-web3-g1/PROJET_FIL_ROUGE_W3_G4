"""Constraint Keys

Revision ID: 30c654563c3d
Revises: 487ee82441c4
Create Date: 2023-07-25 21:31:28.607725

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '30c654563c3d'
down_revision = '487ee82441c4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(op.f('academy_id_key'), 'academy', ['id'])
    op.create_unique_constraint(op.f('annotation_id_key'), 'annotation', ['id'])
    op.create_unique_constraint(op.f('biography_id_key'), 'biography', ['id'])
    op.create_unique_constraint(op.f('biography_meta_id_key'), 'biography_meta', ['id'])
    op.create_unique_constraint(op.f('biography_translation_id_key'), 'biography_translation', ['id'])
    op.create_unique_constraint(op.f('comment_id_key'), 'comment', ['id'])
    op.create_unique_constraint(op.f('image_id_key'), 'image', ['id'])
    op.create_unique_constraint(op.f('image_meta_id_key'), 'image_meta', ['id'])
    op.create_unique_constraint(op.f('masterclass_id_key'), 'masterclass', ['id'])
    op.create_unique_constraint(op.f('masterclass_user_id_key'), 'masterclass_user', ['id'])
    op.create_unique_constraint(op.f('partition_id_key'), 'partition', ['id'])
    op.create_unique_constraint(op.f('partition_meta_id_key'), 'partition_meta', ['id'])
    op.create_unique_constraint(op.f('reset_token_id_key'), 'reset_token', ['id'])
    op.create_unique_constraint(op.f('subtitle_id_key'), 'subtitle', ['id'])
    op.create_unique_constraint(op.f('tag_id_key'), 'tag', ['id'])
    op.create_unique_constraint(op.f('timecode_id_key'), 'timecode', ['id'])
    op.create_unique_constraint(op.f('user_id_key'), 'user', ['id'])
    op.create_unique_constraint(op.f('video_id_key'), 'video', ['id'])
    op.create_unique_constraint(op.f('video_meta_id_key'), 'video_meta', ['id'])
    op.create_unique_constraint(op.f('work_analysis_id_key'), 'work_analysis', ['id'])
    op.create_unique_constraint(op.f('work_analysis_meta_id_key'), 'work_analysis_meta', ['id'])
    op.create_unique_constraint(op.f('work_analysis_translation_id_key'), 'work_analysis_translation', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('work_analysis_translation_id_key'), 'work_analysis_translation', type_='unique')
    op.drop_constraint(op.f('work_analysis_meta_id_key'), 'work_analysis_meta', type_='unique')
    op.drop_constraint(op.f('work_analysis_id_key'), 'work_analysis', type_='unique')
    op.drop_constraint(op.f('video_meta_id_key'), 'video_meta', type_='unique')
    op.drop_constraint(op.f('video_id_key'), 'video', type_='unique')
    op.drop_constraint(op.f('user_id_key'), 'user', type_='unique')
    op.drop_constraint(op.f('timecode_id_key'), 'timecode', type_='unique')
    op.drop_constraint(op.f('tag_id_key'), 'tag', type_='unique')
    op.drop_constraint(op.f('subtitle_id_key'), 'subtitle', type_='unique')
    op.drop_constraint(op.f('reset_token_id_key'), 'reset_token', type_='unique')
    op.drop_constraint(op.f('partition_meta_id_key'), 'partition_meta', type_='unique')
    op.drop_constraint(op.f('partition_id_key'), 'partition', type_='unique')
    op.drop_constraint(op.f('masterclass_user_id_key'), 'masterclass_user', type_='unique')
    op.drop_constraint(op.f('masterclass_id_key'), 'masterclass', type_='unique')
    op.drop_constraint(op.f('image_meta_id_key'), 'image_meta', type_='unique')
    op.drop_constraint(op.f('image_id_key'), 'image', type_='unique')
    op.drop_constraint(op.f('comment_id_key'), 'comment', type_='unique')
    op.drop_constraint(op.f('biography_translation_id_key'), 'biography_translation', type_='unique')
    op.drop_constraint(op.f('biography_meta_id_key'), 'biography_meta', type_='unique')
    op.drop_constraint(op.f('biography_id_key'), 'biography', type_='unique')
    op.drop_constraint(op.f('annotation_id_key'), 'annotation', type_='unique')
    op.drop_constraint(op.f('academy_id_key'), 'academy', type_='unique')
    # ### end Alembic commands ###
