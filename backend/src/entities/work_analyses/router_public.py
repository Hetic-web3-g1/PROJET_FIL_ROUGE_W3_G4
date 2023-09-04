from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.database.db_engine import engine

from .exceptions import (
    WorkAnalysisMetaNotFound,
    WorkAnalysisMetaKeyAlreadyExist,
)
from . import service as work_analysis_service
from .schemas import (
    WorkAnalysisMetaCreate,
)

router = APIRouter(
    prefix="/work_analyzes",
    tags=["WorkAnalysis"],
)


@router.get("")
def get_all_work_analyzes():
    with engine.begin() as conn:
        work_analyzes = work_analysis_service.get_all_work_analyzes(conn)
        return list(work_analyzes)


@router.get("/work_analysis/{work_analysis_id}")
def get_work_analysis_by_id(work_analysis_id: UUID):
    with engine.begin() as conn:
        work_analysis = work_analysis_service.get_work_analysis_by_id(
            conn, work_analysis_id
        )
        return work_analysis


# ---------------------------------------------------------------------------------------------------- #


@router.get("/work_analysis/translation/{work_analysis_translation_id}")
def get_work_analysis_translation_by_id(work_analysis_translation_id: int):
    with engine.begin() as conn:
        work_analysis_translation = (
            work_analysis_service.get_work_analysis_translation_by_id(
                conn, work_analysis_translation_id
            )
        )
        return work_analysis_translation


@router.get("/work_analysis/translation/work_analysis/{work_analysis_id}")
def get_work_analysis_translation_by_work_analysis(work_analysis_id: UUID):
    with engine.begin() as conn:
        work_analysis_translation = (
            work_analysis_service.get_work_analysis_translation_by_work_analysis(
                conn, work_analysis_id
            )
        )
        return work_analysis_translation


# ---------------------------------------------------------------------------------------------------- #


@router.get("/work_analysis/meta/{meta_id}")
def get_work_analysis_meta_by_id(meta_id: int):
    try:
        with engine.begin() as conn:
            meta = work_analysis_service.get_work_analysis_meta_by_id(conn, meta_id)
            return meta

    except WorkAnalysisMetaNotFound:
        raise HTTPException(
            status_code=404,
            detail="Work Analysis meta not found",
        )


@router.get("/work_analysis/meta/work_analysis/{work_analysis_id}")
def get_work_analysis_meta_by_work_analysis_id(work_analysis_id: UUID):
    with engine.begin() as conn:
        meta = work_analysis_service.get_work_analysis_meta_by_work_analysis_id(
            conn, work_analysis_id
        )
        return meta


@router.post("/work_analysis/meta")
def create_work_analysis_meta(meta: WorkAnalysisMetaCreate):
    try:
        with engine.begin() as conn:
            work_analysis_service.create_work_analysis_meta(conn, meta)

    except WorkAnalysisMetaKeyAlreadyExist:
        raise HTTPException(
            status_code=400,
            detail="Meta key already exist",
        )


@router.put("/work_analysis/meta/{meta_id}")
def update_work_analysis_meta(meta_id: int, meta: WorkAnalysisMetaCreate):
    try:
        with engine.begin() as conn:
            work_analysis_service.update_work_analysis_meta(conn, meta_id, meta)

    except WorkAnalysisMetaNotFound:
        raise HTTPException(
            status_code=404,
            detail="Work Analysis meta not found",
        )


@router.delete("/work_analysis/meta/{meta_id}")
def delete_work_analysis_meta(meta_id: int):
    try:
        with engine.begin() as conn:
            work_analysis_service.delete_work_analysis_meta(conn, meta_id)

    except WorkAnalysisMetaNotFound:
        raise HTTPException(
            status_code=404,
            detail="Work Analysis meta not found",
        )
