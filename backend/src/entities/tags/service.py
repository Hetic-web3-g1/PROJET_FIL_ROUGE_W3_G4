import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.engine import Connection

from src.database import service as db_service
from .schemas import Tag, TagCreate
from ..biographies.schemas import Biography
from ..masterclasses.schemas import Masterclass
from ..partitions.schemas import Partition
from ..subtitles.schemas import Subtitle
from ..users.schemas import User
from ..videos.schemas import Video
from ..work_analyses.schemas import WorkAnalysis
from ..biographies.models import biography_tag_table, biography_table
from ..masterclasses.models import masterclass_table, masterclass_tag_table
from ..partitions.models import partition_table, partition_tag_table
from ..subtitles.models import subtitle_table, subtitle_tag_table
from ..users.models import user_table, user_tag_table
from ..videos.models import video_table, video_tag_table
from ..work_analyses.models import work_analysis_table, work_analysis_tag_table
from ..users.schemas import User
from .models import tag_table
from src.database.db_engine import metadata


def _parse_row(row: sa.Row):
    return Tag(**row._asdict())


def _parse_row_specific_object(row: sa.Row, object_entity):
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


def create_tag(conn: Connection, tag: TagCreate, user: User) -> Tag:
    """
    Create a tag.

    Args:
        tag (TagCreate): TagCreate object.
        user (User): The user creating the tag.

    Returns:
        Tag: The created Tag object.
    """
    result = db_service.create_object(conn, tag_table, tag.dict())
    return _parse_row(result)


def create_link_table(conn: Connection, entity, entity_table, user: User):
    """
    Link Tag to entity.

    Args:
        entity (Entity): Entity object.
        user (User): The user creating the tag.

    Returns:
        Entity: The created Entity object.
    """
    result = db_service.create_object(conn, entity_table, entity.dict())
    return result
