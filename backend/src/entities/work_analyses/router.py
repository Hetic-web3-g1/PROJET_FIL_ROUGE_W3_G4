from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.database.db_engine import engine

from ..authentification.dependencies import CustomSecurity
from ..comments.schemas import CommentCreate
from ..users.schemas import User
from .exceptions import WorkAnalysisNotFound
from . import service as work_analysis_service
from .schemas import WorkAnalysisCreate

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

    except WorkAnalysisNotFound:
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

    except WorkAnalysisNotFound:
        raise HTTPException(
            status_code=404,
            detail="Work Analysis not found",
        )


# ---------------------------------------------------------------------------------------------------- #


@router.post("/work_analysis/comment/{work_analysis_id}")
def create_work_analysis_comment(
    comment: CommentCreate, work_analysis_id, user: User = Depends(CustomSecurity())
):
    with engine.begin() as conn:
        work_analysis_service.create_work_analysis_comment(
            conn, comment, work_analysis_id, user
        )
