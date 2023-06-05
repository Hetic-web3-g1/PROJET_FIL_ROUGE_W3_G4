from fastapi import APIRouter
from typing import List, Union

from database.db_engine import engine
from schema.response import ResponseModel
from utils.route_function import check_id, route_response, get_route_response
from schema.work_analysis import WorkAnalysis, WorkAnalysisCreate, WorkAnalysisUpdate
from manager import work_analysis_manager

router = APIRouter(
    prefix="/work_analysis",
    tags=["Work Analysis"],
)

# Get all work_analyses
@router.get("", response_model=Union[List[WorkAnalysis], None])
def get_all_work_analyses():
    with engine.begin() as conn:
        response = list(work_analysis_manager.get_all_work_analysis(conn))
        return get_route_response(response, 200, 404, "No work_analyses found")

# Get work_analysis by id
@router.get("/{work_analysis_id}", response_model=Union[WorkAnalysis, None])
def get_work_analysis_by_id(work_analysis_id: str):
    check_id(work_analysis_id)
    with engine.begin() as conn:
        response = work_analysis_manager.get_work_analysis_by_id(conn, work_analysis_id)
        return get_route_response(response, 200, 404, "WorkAnalysis not found")

# Create work_analysis
@router.post("", response_model=ResponseModel)
def create_work_analysis(work_analysis: WorkAnalysisCreate):
    with engine.begin() as conn:
        response = work_analysis_manager.create_work_analysis(conn, work_analysis)
        return route_response(response, 200, 500)

# Update work_analysis
@router.put("/{work_analysis_id}", response_model=ResponseModel)
def update_work_analysis(work_analysis_id: str, work_analysis: WorkAnalysisUpdate):
    check_id(work_analysis_id)
    with engine.begin() as conn:
        response = work_analysis_manager.update_work_analysis(conn, work_analysis_id, work_analysis)
        return route_response(response, 200, 500)

# Delete work_analysis
@router.delete("/{work_analysis_id}", response_model=ResponseModel)
def delete_work_analysis(work_analysis_id: str):
    check_id(work_analysis_id)
    with engine.begin() as conn:
        response = work_analysis_manager.delete_work_analysis(conn, work_analysis_id)
        return route_response(response, 200, 500)