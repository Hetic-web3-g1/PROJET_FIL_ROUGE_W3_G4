from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from src.database import db_srv
from src.database.db_engine import engine
from .schemas import WorkAnalysis, WorkAnalysisCreate
from .models import work_analysis_table
from ..users.models import user_table
from .exceptions import WorkAnalysisNotFound


def _parse_row(row: sa.Row):
    return WorkAnalysis(**row._asdict())


def get_all_work_analysis(conn: Connection):
    """
    Get all work_analysis.

    Returns:
        WorkAnalysis: Dict of WorkAnalysis objects.
    """
    response = conn.execute(sa.select(work_analysis_table)).fetchall()
    return [_parse_row(row) for row in response]


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
    response = conn.execute(
        sa.select(work_analysis_table).where(work_analysis_table.c.id == work_analysis_id)
    ).first()
    if response is None:
        raise WorkAnalysisNotFound

    return _parse_row(response)


def create_work_analysis(conn: Connection, work_analysis: WorkAnalysisCreate) -> None:
    """
    Create a work_analysis.

    Args:
        work_analysis (WorkAnalysisCreate): WorkAnalysisCreate object.

    Returns:
        WorkAnalysis: The created WorkAnalysis object.
    """
    db_srv.create_object(conn, work_analysis_table, work_analysis.dict())