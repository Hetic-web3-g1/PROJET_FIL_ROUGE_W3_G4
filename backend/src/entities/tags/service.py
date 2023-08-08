import sqlalchemy as sa
from sqlalchemy.engine import Connection
from sqlalchemy.sql import func
from src.database import service as db_service
from src.database.db_engine import metadata
from src.utils.string_utils import sanitizeAndLowerCase

from ..biographies.models import biography_table, biography_tag_table
from ..biographies.schemas import Biography
from ..masterclasses.models import masterclass_table, masterclass_tag_table
from ..masterclasses.schemas import Masterclass
from ..partitions.models import partition_table, partition_tag_table
from ..partitions.schemas import Partition
from ..subtitles.models import subtitle_table, subtitle_tag_table
from ..subtitles.schemas import Subtitle
from ..users.models import user_table, user_tag_table
from ..users.schemas import User
from ..videos.models import video_table, video_tag_table
from ..videos.schemas import Video
from ..work_analyses.models import work_analysis_table, work_analysis_tag_table
from ..work_analyses.schemas import WorkAnalysis
from .models import tag_table
from .schemas import Tag, TagCreate


def _parse_row(row: sa.Row):
    return Tag(**row._asdict())


def _parse_row_specific_object(row: sa.Row, object_entity):  # type: ignore
    return object_entity(**row._asdict())


def search_by_table(conn: Connection, search, tables):
    """
    Search for a Tag in a list of tables.

    Args:
        search (str): Search string.
        tables (List[str]): List of tables to search in.

    Returns:
        List[Search]: List of objects.
    """
    objects = {
        "biography": {
            "table": biography_table,
            "object_id": "biography_id",
            "tag_table": biography_tag_table,
            "entity": Biography,
        },
        "masterclass": {
            "table": masterclass_table,
            "object_id": "masterclass_id",
            "tag_table": masterclass_tag_table,
            "entity": Masterclass,
        },
        "partition": {
            "table": partition_table,
            "object_id": "partition_id",
            "tag_table": partition_tag_table,
            "entity": Partition,
        },
        "subtitle": {
            "table": subtitle_table,
            "object_id": "subtitle_id",
            "tag_table": subtitle_tag_table,
            "entity": Subtitle,
        },
        "user": {
            "table": user_table,
            "object_id": "user_id",
            "tag_table": user_tag_table,
            "entity": User,
        },
        "video": {
            "table": video_table,
            "object_id": "video_id",
            "tag_table": video_tag_table,
            "entity": Video,
        },
        "work_analysis": {
            "table": work_analysis_table,
            "object_id": "work_analysis_id",
            "tag_table": work_analysis_tag_table,
            "entity": WorkAnalysis,
        },
    }

    cte_query = []
    result = []
    for table in tables:
        object_table = objects[table]["table"]
        object_tag_table = objects[table]["tag_table"]
        object_id = objects[table]["object_id"]
        object_entity = objects[table]["entity"]

        cte_query = (
            sa.select(object_table, func.array_agg(tag_table.c.content).label("tags"))
            .select_from(
                object_table.join(
                    object_tag_table,
                    object_table.c.id == object_tag_table.c[object_id],
                ).join(tag_table, tag_table.c.id == object_tag_table.c.tag_id)
            )
            .group_by(object_table.c.id)
            .cte(f"{table}_cte")
        )

        table = sa.select(cte_query).where(
            func.lower(func.array_to_string(cte_query.c.tags, ",")).like(
                func.lower(f"%{search}%")
            )
        )

        response = conn.execute(table).fetchall()
        result.append(
            [_parse_row_specific_object(row, object_entity) for row in response]
        )

    return result

    # def search_by_table(conn: Connection, search, tables):


#     """
#     Search for a Tag in a list of tables.

#     Args:
#         search (str): Search string.
#         tables (List[str]): List of tables to search in.

#     Returns:
#         List[Search]: List of Search objects.
#     """
#     query = sa.select(tag_table).where(
#         tag_table.c.content.ilike(f"{search}%") & tag_table.c.tag_type.in_(tables)
#     )

#     result = conn.execute(query).fetchall()
#     return [_parse_row(row) for row in result]


def search_object_by_tag(conn: Connection, tag: Tag):
    """
    Search for an object with a Tag.

    Args:
        Tag (Tag): Tag object.

    Returns:
        Object: Object.
    """
    query = sa.select(metadata.tables[tag.tag_type]).where(tag_table.c.id == tag.id)
    result = conn.execute(query).fetchone()
    if result:
        column_names = metadata.tables[tag.tag_type].columns.keys()
        data = {column: value for column, value in zip(column_names, result)}
        return {tag.tag_type: data}

    return None


def search_tags_by_object(conn: Connection, object_id, object_table, object_tag_table):
    """
    Search for Tags linked to an object.

    Args:
        object_id (int): Id of object.
        object_table (Table): Table of object.
        object_tag_table (Table): Table linking tag to object.

    Returns:
        List[Tag]: List of Tag objects.
    """
    query = (
        sa.select(tag_table)
        .select_from(
            tag_table.join(
                object_tag_table, tag_table.c.id == object_tag_table.c.tag_id
            ).join(object_table, object_table.c.id == object_tag_table.c.entity_id)
        )
        .where(object_table.c.id == object_id)
    )

    result = conn.execute(query).fetchall()
    for row in result:
        yield _parse_row(row)


def create_tag(conn: Connection, tag: TagCreate) -> Tag:
    """
    Create a tag.

    Args:
        tag (TagCreate): TagCreate object.

    Returns:
        Tag: The created Tag object.
    """
    result = db_service.create_object(conn, tag_table, tag.dict())
    return _parse_row(result)


def create_link_table(conn: Connection, entity, entity_table):
    """
    Link Tag to entity.

    Args:
        entity (Entity): Entity object.
        entity_table (Table): Table of entity.

    Returns:
        Entity: The created Entity object.
    """
    result = db_service.create_object(conn, entity_table, entity.dict())
    return result


def create_tag_and_link_table(
    conn: Connection, content, object_table, object, object_tag_table, object_id
):
    """
    Create a tag and link it to an object.

    Args:
        content (str): Content of the tag.
        object_table (Table): Table of object.
        object_tag_table (Table): Table linking tag to object.
        object (object): Object.
        object_id (int): Id of object.
    """
    tag = TagCreate(content=sanitizeAndLowerCase(content), tag_type=str(object_table))

    created_tag = create_tag(conn, tag)

    entity_tag = object_tag_table(
        entity_id=object_id,
        tag_id=created_tag.id,
    )
    create_link_table(conn, entity_tag, object)


def delete_tags_by_object_id(
    conn: Connection, object_id, object_table, object_tag_table
):
    """
    Delete tags linked to an object.

    Args:
        object_id (int): Id of object.
        object_table (Table): Table of object.
        object_tag_table (Table): Table linking tag to object.
    """
    result = search_tags_by_object(conn, object_id, object_table, object_tag_table)
    tag_ids = [tag.id for tag in result]
    db_service.delete_objects(conn, tag_table, tag_ids)


# DEPRECIATED
def delete_orphaned_tags(conn: Connection, link_table, entity_table):
    """
    Delete orphaned tags.

    Args:
        link_table (Table): Table linking tag to entity.
        entity_table (Table): Table of entity.
    """
    orphaned_tags = conn.execute(
        sa.select(tag_table).where(
            (tag_table.c.tag_type == str(entity_table))
            & sa.not_(tag_table.c.id.in_(sa.select(link_table.c.tag_id)))
        )
    ).fetchall()
    orphaned_tag_ids = [tag.id for tag in orphaned_tags]
    db_service.delete_objects(conn, tag_table, orphaned_tag_ids)
