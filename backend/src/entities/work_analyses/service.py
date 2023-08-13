from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.engine import Connection
from src.database import service as db_service

from ..comments import service as comment_service
from ..comments.schemas import CommentCreate, WorkAnalysisComment
from ..tags import service as tag_service
from ..tags.schemas import WorkAnalysisTag
from ..users.schemas import User
from .exceptions import (
    WorkAnalysisNotFound,
    WorkAnalysisMetaNotFound,
    WorkAnalysisMetaKeyAlreadyExist,
)
from .models import (
    work_analysis_table,
    work_analysis_tag_table,
    work_analysis_comment_table,
    work_analysis_meta_table,
)
from .schemas import (
    WorkAnalysis,
    WorkAnalysisCreate,
    WorkAnalysisMeta,
    WorkAnalysisMetaCreate,
)


def _parse_row(row: sa.Row):
    return WorkAnalysis(**row._asdict())


def _parse_meta_row(row: sa.Row):
    return WorkAnalysisMeta(**row._asdict())


def get_all_work_analyzes(conn: Connection):
    """
    Get all work_analyzes.

    Returns:
        WorkAnalysis: Dict of WorkAnalysis objects.
    """
    result = conn.execute(sa.select(work_analysis_table)).fetchall()
    for row in result:
        yield _parse_row(row)


def get_work_analysis_by_id(conn: Connection, work_analysis_id: UUID) -> WorkAnalysis:
    """
    Get a work_analysis by the given id.

    Args:
        work_analysis_id (UUID): The id of the work_analysis.

    Returns:
        WorkAnalysis: The WorkAnalysis object.

    Raises:
        WorkAnalysisNotFound: If the work_analysis does not exist.
    """
    result = conn.execute(
        sa.select(work_analysis_table).where(
            work_analysis_table.c.id == work_analysis_id
        )
    ).first()
    if result is None:
        raise WorkAnalysisNotFound

    return _parse_row(result)


def create_work_analysis_tags(conn, work_analysis: WorkAnalysis) -> None:
    """
    Create tags for a work_analysis.

    Args:
        work_analysis (WorkAnalysisCreate): WorkAnalysisCreate object.
        result (sa.Row): Result of work_analysis creation.
    """
    tags = [work_analysis.title]

    for content in tags:
        tag_service.create_tag_and_link_table(
            conn,
            content,
            work_analysis_table,
            work_analysis_tag_table,
            WorkAnalysisTag,
            work_analysis.id,
        )


def create_work_analysis(
    conn: Connection, work_analysis: WorkAnalysisCreate, user: User
) -> WorkAnalysis:
    """
    Create a work_analysis.

    Args:
        work_analysis (WorkAnalysisCreate): WorkAnalysisCreate object.
        user (User): The user creating the work_analysis.

    Returns:
        WorkAnalysis: The created WorkAnalysis object.
    """
    result = db_service.create_object(
        conn, work_analysis_table, work_analysis.dict(), user_id=user.id
    )

    work_analysis = _parse_row(result)
    create_work_analysis_tags(conn, work_analysis)

    return _parse_row(result)


def update_work_analysis(
    conn: Connection,
    work_analysis_id: UUID,
    work_analysis: WorkAnalysisCreate,
    user: User,
) -> WorkAnalysis:
    """
    Update a work_analysis.

    Args:
        work_analysis_id (UUID): The id of the work_analysis.
        work_analysis (WorkAnalysisCreate): WorkAnalysisCreate object.
        user (User): The user updating the work_analysis.

    Returns:
        WorkAnalysis: The updated WorkAnalysis object.

    Raises:
        WorkAnalysisNotFound: If the work_analysis does not exist.
    """
    check = conn.execute(
        sa.select(work_analysis_table).where(
            work_analysis_table.c.id == work_analysis_id
        )
    ).first()
    if check is None:
        raise WorkAnalysisNotFound

    result = db_service.update_object(
        conn,
        work_analysis_table,
        work_analysis_id,
        work_analysis.dict(),
        user_id=user.id,
    )

    tag_service.delete_tags_by_object_id(
        conn, work_analysis_id, work_analysis_table, work_analysis_tag_table
    )

    work_analysis = _parse_row(result)
    create_work_analysis_tags(conn, work_analysis)

    return _parse_row(result)


def delete_work_analysis(conn: Connection, work_analysis_id: UUID) -> None:
    """
    Delete a work_analysis.

    Args:
        work_analysis_id (UUID): The id of the work_analysis.

    Raises:
        WorkAnalysisNotFound: If the work_analysis does not exist.
    """
    check = conn.execute(
        sa.select(work_analysis_table).where(
            work_analysis_table.c.id == work_analysis_id
        )
    ).first()
    if check is None:
        raise WorkAnalysisNotFound

    tag_service.delete_tags_by_object_id(
        conn, work_analysis_id, work_analysis_table, work_analysis_tag_table
    )
    comment_service.delete_comments_by_object_id(
        conn, work_analysis_id, work_analysis_table, work_analysis_comment_table
    )
    db_service.delete_object(conn, work_analysis_table, work_analysis_id)


# ---------------------------------------------------------------------------------------------------- #


def create_work_analysis_comment(
    conn: Connection, comment: CommentCreate, work_analysis_id: UUID, user: User
):
    """
    Create a comment and link it to a work_analysis.

    Args:
        comment (CommentCreate): CommentCreate object.
        work_analysis_id (UUID): Id of work_analysis.
        user (User): The user creating the comment.
    """
    comment_service.create_comment_and_link_table(
        conn,
        comment,
        work_analysis_comment_table,
        WorkAnalysisComment,
        work_analysis_id,
        user,
    )


# ---------------------------------------------------------------------------------------------------- #


def get_work_analysis_meta_by_id(conn: Connection, meta_id: int) -> WorkAnalysisMeta:
    """
    Get a work_analysis_meta by the given id.

    Args:
        meta_id (int): The id of the work_analysis_meta.

    Raises:
        WorkAnalysisMetaNotFound: If the work_analysis_meta does not exist.

    Returns:
        WorkAnalysisMeta: The WorkAnalysisMeta object.
    """
    result = conn.execute(
        sa.select(work_analysis_meta_table).where(
            work_analysis_meta_table.c.id == meta_id
        )
    ).first()
    if result is None:
        raise WorkAnalysisMetaNotFound

    return _parse_meta_row(result)


def get_work_analysis_meta_by_work_analysis_id(
    conn: Connection, work_analysis_id: UUID
) -> list[WorkAnalysisMeta]:
    """
    Get all work_analysis_meta for a work_analysis.

    Args:
        work_analysis_id (UUID): The id of the work_analysis.

    Returns:
        list[WorkAnalysisMeta]: List of WorkAnalysisMeta objects.
    """
    result = conn.execute(
        sa.select(work_analysis_meta_table).where(
            work_analysis_meta_table.c.work_analysis_id == work_analysis_id
        )
    ).fetchall()

    return [_parse_meta_row(row) for row in result]


def create_work_analysis_meta(
    conn: Connection, meta: WorkAnalysisMetaCreate
) -> WorkAnalysisMeta:
    """
    Create a work_analysis_meta for a work_analysis.

    Args:
        meta (WorkAnalysisMetaCreate): WorkAnalysisMetaCreate object.

    Returns:
        WorkAnalysisMeta: The created WorkAnalysisMeta object.

    Raises:
        WorkAnalysisMetaKeyAlreadyExist: If the key already exists.
    """
    check = conn.execute(
        sa.select(work_analysis_meta_table).where(
            work_analysis_meta_table.c.meta_key == meta.meta_key,
        )
    ).first()
    if check is not None:
        raise WorkAnalysisMetaKeyAlreadyExist

    result = db_service.create_object(conn, work_analysis_meta_table, meta.dict())

    return _parse_meta_row(result)


def update_work_analysis_meta(
    conn: Connection, meta_id: int, meta: WorkAnalysisMetaCreate
) -> WorkAnalysisMeta:
    """
    Update a work_analysis_meta.

    Args:
        meta_id (int): The id of the work_analysis_meta.
        meta (WorkAnalysisMetaCreate): WorkAnalysisMetaCreate object.

    Returns:
        WorkAnalysisMeta: The updated WorkAnalysisMeta object.

    Raises:
        WorkAnalysisMetaNotFound: If the work_analysis_meta does not exist.
    """
    check = conn.execute(
        sa.select(work_analysis_meta_table).where(
            work_analysis_meta_table.c.id == meta_id
        )
    ).first()
    if check is None:
        raise WorkAnalysisMetaNotFound

    result = db_service.update_object(
        conn, work_analysis_meta_table, meta_id, meta.dict()
    )

    return _parse_meta_row(result)


def delete_work_analysis_meta(conn: Connection, meta_id: int) -> None:
    """
    Delete a work_analysis_meta.

    Args:
        meta_id (int): The id of the work_analysis_meta.

    Raises:
        WorkAnalysisMetaNotFound: If the work_analysis_meta does not exist.
    """
    check = conn.execute(
        sa.select(work_analysis_meta_table).where(
            work_analysis_meta_table.c.id == meta_id
        )
    ).first()
    if check is None:
        raise WorkAnalysisMetaNotFound

    db_service.delete_object(conn, work_analysis_meta_table, meta_id)
