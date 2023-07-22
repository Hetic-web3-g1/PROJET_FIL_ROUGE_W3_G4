from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from src.database import db_srv
from .schemas import WorkAnalysis, WorkAnalysisCreate
from ..users.schemas import User
from .models import work_analysis_table
from .exceptions import WorkAnalysisNotFound


def _parse_row(row: sa.Row):
    return WorkAnalysis(**row._asdict())


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
    result = db_srv.create_object(
        conn, work_analysis_table, work_analysis.dict(), user_id=user.id
    )
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

    result = db_srv.update_object(
        conn,
        work_analysis_table,
        work_analysis_id,
        work_analysis.dict(),
        user_id=user.id,
    )
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

    db_srv.delete_object(conn, work_analysis_table, work_analysis_id)

    # ('483f0848-320b-44b0-9008-da1064082d0c', 'Yes', ['Smit'], 'Youpilapin', 'created', '2023-07-14 16:11:47.089795', '2023-07-14 16:14:41.985109', '12345648-1234-1234-1234-123456789123', '12345648-1234-1234-1234-123456789123')
    # (UUID('5a28f399-6b6b-4d3b-85c6-f7d4005e212b'), 'Yes', ['Smit'], 'Youpi', 'created', datetime.datetime(2023, 7, 14, 16, 15, 7, 32526), None, UUID('12345648-1234-1234-1234-123456789123'), None)
