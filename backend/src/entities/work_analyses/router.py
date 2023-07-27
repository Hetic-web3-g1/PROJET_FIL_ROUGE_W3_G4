from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID

from .schemas import WorkAnalysisCreate
from ..users.schemas import User
from . import exceptions as work_analysis_exceptions
from . import service as work_analysis_service
from src.database.db_engine import engine
from ..authentification.dependencies import CustomSecurity

router = APIRouter(
    prefix="/work_analyzes",
    tags=["WorkAnalysis"],
)


@router.get("")
def get_all_work_analyzes(
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        work_analyzes = work_analysis_service.get_all_work_analyzes(conn)
        return list(work_analyzes)


@router.get("/work_analysis/{work_analysis_id}")
def get_work_analysis_by_id(
    work_analysis_id: UUID,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        work_analysis = work_analysis_service.get_work_analysis_by_id(
            conn, work_analysis_id
        )
        return work_analysis


@router.post("/work_analysis")
def create_work_analysis(
    new_work_analysis: WorkAnalysisCreate, user: User = Depends(CustomSecurity())
):
    with engine.begin() as conn:
        return work_analysis_service.create_work_analysis(conn, new_work_analysis, user)


@router.put("/work_analysis/{work_analysis_id}")
def update_work_analysis(
    work_analysis_id: UUID,
    work_analysis: WorkAnalysisCreate,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            work_analysis_service.update_work_analysis(
                conn, work_analysis_id, work_analysis, user
            )

    except work_analysis_exceptions.WorkAnalysisNotFound:
        raise HTTPException(
            status_code=404,
            detail="Work Analysis not found",
        )


@router.delete("/work_analysis/{work_analysis_id}")
def delete_work_analysis(
    work_analysis_id: UUID, user: User = Depends(CustomSecurity())
):
    try:
        with engine.begin() as conn:
            work_analysis_service.delete_work_analysis(conn, work_analysis_id)

    except work_analysis_exceptions.WorkAnalysisNotFound:
        raise HTTPException(
            status_code=404,
            detail="Work Analysis not found",
        )
