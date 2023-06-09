from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID

from .schemas import WorkAnalysis, WorkAnalysisCreate
from ..users.schemas import User
from . import exceptions as work_analysis_exceptions
from . import service as work_analysis_service
from src.database.db_engine import engine
from ..authentification import service as auth_service
from ..authentification.dependencies import CustomSecurity

router = APIRouter(
    prefix="/work_analyses",
    tags=["WorkAnalysis"],
)


# Get all work_analysis
@router.get("")
def get_all_work_analysis(
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        response = work_analysis_service.get_all_work_analysis(conn)
        return response


# Get work_analysis by id
@router.get("/{work_analysis_id}")
def get_work_analysis_by_id(
    work_analysis_id: UUID,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        response = work_analysis_service.get_work_analysis_by_id(conn, work_analysis_id)
        return response


# Create work_analysis
@router.post("/work_analysis")
def create_work_analysis(
    new_work_analysis: WorkAnalysisCreate, User: User = Depends(CustomSecurity())
):
    with engine.begin() as conn:
        new_work_analysis = work_analysis_service.create_work_analysis(conn, new_work_analysis)