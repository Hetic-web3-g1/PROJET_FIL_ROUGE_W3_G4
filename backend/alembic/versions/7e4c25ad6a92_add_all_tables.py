"""Add all tables

Revision ID: 7e4c25ad6a92
Revises: 3d3845c9e048
Create Date: 2023-07-10 13:01:02.481737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e4c25ad6a92'
down_revision = '3d3845c9e048'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('annotation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('measure', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.UUID(), nullable=False),
    sa.Column('updated_by', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['updated_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.UUID(), nullable=False),
    sa.Column('updated_by', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['updated_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('image',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('file_name', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.UUID(), nullable=False),
    sa.Column('updated_by', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['updated_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('partition',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('file_name', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.UUID(), nullable=False),
    sa.Column('updated_by', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['updated_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('video',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('version', sa.Float(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('duration', sa.Float(), nullable=True),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('file_name', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.UUID(), nullable=False),
    sa.Column('updated_by', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['updated_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('work_analysis',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('about', sa.Text(), nullable=True),
    sa.Column('learning', sa.ARRAY(sa.String(), dimensions=1), nullable=True),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.UUID(), nullable=False),
    sa.Column('updated_by', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['updated_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('biography',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('instrument', sa.ARRAY(sa.String(), dimensions=1), nullable=True),
    sa.Column('nationality', sa.String(), nullable=True),
    sa.Column('website', sa.String(), nullable=True),
    sa.Column('award', sa.ARRAY(sa.String(), dimensions=1), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('image_id', sa.UUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.UUID(), nullable=False),
    sa.Column('updated_by', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['image_id'], ['image.id'], ),
    sa.ForeignKeyConstraint(['updated_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('image_meta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_id', sa.UUID(), nullable=False),
    sa.Column('meta_key', sa.String(), nullable=False),
    sa.Column('meta_value', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['image.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('partition_annotation',
    sa.Column('partition_id', sa.UUID(), nullable=False),
    sa.Column('annotation_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['annotation_id'], ['annotation.id'], ),
    sa.ForeignKeyConstraint(['partition_id'], ['partition.id'], )
    )
    op.create_table('partition_comment',
    sa.Column('partition_id', sa.UUID(), nullable=False),
    sa.Column('comment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['comment_id'], ['comment.id'], ),
    sa.ForeignKeyConstraint(['partition_id'], ['partition.id'], )
    )
    op.create_table('partition_meta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('partition_id', sa.UUID(), nullable=False),
    sa.Column('meta_key', sa.String(), nullable=False),
    sa.Column('meta_value', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['partition_id'], ['partition.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('partition_tag',
    sa.Column('partition_id', sa.UUID(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['partition_id'], ['partition.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], )
    )
    op.create_table('subtitle',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('video_id', sa.UUID(), nullable=False),
    sa.Column('language', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('file_name', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.UUID(), nullable=False),
    sa.Column('updated_by', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['updated_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['video_id'], ['video.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('timecode',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('video_id', sa.UUID(), nullable=False),
    sa.Column('hour', sa.Integer(), nullable=True),
    sa.Column('minute', sa.Integer(), nullable=True),
    sa.Column('second', sa.Integer(), nullable=True),
    sa.Column('frame', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['video_id'], ['video.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('video_comment',
    sa.Column('video_id', sa.UUID(), nullable=False),
    sa.Column('comment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['comment_id'], ['comment.id'], ),
    sa.ForeignKeyConstraint(['video_id'], ['video.id'], )
    )
    op.create_table('video_meta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('video_id', sa.UUID(), nullable=False),
    sa.Column('meta_key', sa.String(), nullable=False),
    sa.Column('meta_value', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['video_id'], ['video.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('video_tag',
    sa.Column('video_id', sa.UUID(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.ForeignKeyConstraint(['video_id'], ['video.id'], )
    )
    op.create_table('work_analysis_comment',
    sa.Column('work_analysis_id', sa.UUID(), nullable=False),
    sa.Column('comment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['comment_id'], ['comment.id'], ),
    sa.ForeignKeyConstraint(['work_analysis_id'], ['work_analysis.id'], )
    )
    op.create_table('work_analysis_meta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('work_analysis_id', sa.UUID(), nullable=False),
    sa.Column('meta_key', sa.String(), nullable=False),
    sa.Column('meta_value', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['work_analysis_id'], ['work_analysis.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('work_analysis_tag',
    sa.Column('work_analysis_id', sa.UUID(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.ForeignKeyConstraint(['work_analysis_id'], ['work_analysis.id'], )
    )
    op.create_table('work_analysis_translation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('work_analysis_id', sa.UUID(), nullable=False),
    sa.Column('language', sa.String(), nullable=False),
    sa.Column('about', sa.Text(), nullable=True),
    sa.Column('learning', sa.ARRAY(sa.String(), dimensions=1), nullable=True),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.UUID(), nullable=False),
    sa.Column('updated_by', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['updated_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['work_analysis_id'], ['work_analysis.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('biography_comment',
    sa.Column('biography_id', sa.UUID(), nullable=False),
    sa.Column('comment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['biography_id'], ['biography.id'], ),
    sa.ForeignKeyConstraint(['comment_id'], ['comment.id'], )
    )
    op.create_table('biography_meta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('biography_id', sa.UUID(), nullable=False),
    sa.Column('meta_key', sa.String(), nullable=False),
    sa.Column('meta_value', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['biography_id'], ['biography.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('biography_tag',
    sa.Column('biography_id', sa.UUID(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['biography_id'], ['biography.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], )
    )
    op.create_table('biography_translation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('biography_id', sa.UUID(), nullable=False),
    sa.Column('language', sa.String(), nullable=False),
    sa.Column('award', sa.ARRAY(sa.String(), dimensions=1), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.UUID(), nullable=False),
    sa.Column('updated_by', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['biography_id'], ['biography.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['updated_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('subtitle_comment',
    sa.Column('subtitle_id', sa.UUID(), nullable=False),
    sa.Column('comment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['comment_id'], ['comment.id'], ),
    sa.ForeignKeyConstraint(['subtitle_id'], ['subtitle.id'], )
    )
    op.create_table('subtitle_tag',
    sa.Column('subtitle_id', sa.UUID(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['subtitle_id'], ['subtitle.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subtitle_tag')
    op.drop_table('subtitle_comment')
    op.drop_table('biography_translation')
    op.drop_table('biography_tag')
    op.drop_table('biography_meta')
    op.drop_table('biography_comment')
    op.drop_table('work_analysis_translation')
    op.drop_table('work_analysis_tag')
    op.drop_table('work_analysis_meta')
    op.drop_table('work_analysis_comment')
    op.drop_table('video_tag')
    op.drop_table('video_meta')
    op.drop_table('video_comment')
    op.drop_table('timecode')
    op.drop_table('subtitle')
    op.drop_table('partition_tag')
    op.drop_table('partition_meta')
    op.drop_table('partition_comment')
    op.drop_table('partition_annotation')
    op.drop_table('image_meta')
    op.drop_table('biography')
    op.drop_table('work_analysis')
    op.drop_table('video')
    op.drop_table('partition')
    op.drop_table('image')
    op.drop_table('comment')
    op.drop_table('annotation')
    op.drop_table('tag')
    # ### end Alembic commands ###
