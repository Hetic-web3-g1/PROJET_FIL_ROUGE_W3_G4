from sqlalchemy.engine import Connection
from sqlalchemy import select
from typing import Union, Generator
from uuid import uuid4

from src.database import db_srv
from src.schema.work_analysis import WorkAnalysis, WorkAnalysisCreate, WorkAnalysisUpdate
from src.database.tables.work_analysis import work_analysis_table

def get_all_work_analysis(conn: Connection) -> Generator[WorkAnalysis, None, None]:
    result = conn.execute(select(work_analysis_table))
    if result is None:
        return
    else:
        for work_analysis_row in result:
            work_analysis_dict = work_analysis_row._asdict()
            yield WorkAnalysis(**work_analysis_dict)

def get_work_analysis_by_id(conn: Connection, work_analysis_id: str) -> Union[WorkAnalysis, None]:
    result = conn.execute(select(work_analysis_table).where(work_analysis_table.c.id == work_analysis_id))
    work_analysis_row = result.fetchone()
    if work_analysis_row is None:
        return None
    else:
        work_analysis_dict = work_analysis_row._asdict()
        return WorkAnalysis(**work_analysis_dict)

def create_work_analysis(conn: Connection, work_analysis: WorkAnalysisCreate):
    try:
        result = db_srv.create_object(conn, 'work_analysis', work_analysis, object_id=uuid4())
        return {"status": "success", "message": "WorkAnalysis created successfully", "value": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def update_work_analysis(conn: Connection, work_analysis_id: str, work_analysis: WorkAnalysisUpdate):
    try:
        filtered_work_analysis = {k: v for k, v in work_analysis.dict().items() if v is not None}
        result = db_srv.update_object(conn, 'work_analysis', work_analysis_id, filtered_work_analysis)
        return {"status": "success", "message": "WorkAnalysis updated successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def delete_work_analysis(conn: Connection, work_analysis_id: str):
    try:
        result = db_srv.delete_object(conn, 'work_analysis', work_analysis_id)
        return {"status": "success", "message": "WorkAnalysis deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}