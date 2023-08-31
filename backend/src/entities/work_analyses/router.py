from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.database.db_engine import engine

from ..authentification.dependencies import CustomSecurity
from ..comments.schemas import CommentCreate
from ..users.schemas import User
from .exceptions import (
    WorkAnalysisNotFound,
    WorkAnalysisTranslationNotFound,
    WorkAnalysisTranslationAlreadyExist,
    WorkAnalysisMetaNotFound,
    WorkAnalysisMetaKeyAlreadyExist,
)
from . import service as work_analysis_service
from .schemas import (
    WorkAnalysisCreate,
    WorkAnalysisTranslationCreate,
    WorkAnalysisMetaCreate,
)

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
        work_analysis = work_analysis_service.create_work_analysis(
            conn, new_work_analysis, user
        )
        return work_analysis.id


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


@router.get("/work_analysis/translation/{work_analysis_translation_id}")
def get_work_analysis_translation_by_id(
    work_analysis_translation_id: int,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        work_analysis_translation = (
            work_analysis_service.get_work_analysis_translation_by_id(
                conn, work_analysis_translation_id
            )
        )
        return work_analysis_translation


@router.get("/work_analysis/translation/work_analysis/{work_analysis_id}")
def get_work_analysis_translation_by_work_analysis(
    work_analysis_id: UUID,
    user: User = Depends(CustomSecurity),
):
    with engine.begin() as conn:
        work_analysis_translation = (
            work_analysis_service.get_work_analysis_translation_by_work_analysis(
                conn, work_analysis_id
            )
        )
        return work_analysis_translation


@router.post("/work_analysis/translation")
def create_work_analysis_translation(
    work_analysis_translation: WorkAnalysisTranslationCreate,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            return work_analysis_service.create_work_analysis_translation(
                conn, work_analysis_translation, user
            )

    except WorkAnalysisTranslationAlreadyExist:
        raise HTTPException(
            status_code=409,
            detail="Translation already exist",
        )


@router.put("/work_analysis/translation/{work_analysis_translation_id}")
def update_work_analysis_translation(
    work_analysis_translation_id: int,
    work_analysis_translation: WorkAnalysisTranslationCreate,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            return work_analysis_service.update_work_analysis_translation(
                conn, work_analysis_translation_id, work_analysis_translation, user
            )

    except WorkAnalysisTranslationNotFound:
        raise HTTPException(
            status_code=404,
            detail="Translation not found",
        )


@router.delete("/work_analysis/translation/{work_analysis_translation_id}")
def delete_work_analysis_translation(
    work_analysis_translation_id: int,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            return work_analysis_service.delete_work_analysis_translation(
                conn, work_analysis_translation_id
            )

    except WorkAnalysisTranslationNotFound:
        raise HTTPException(
            status_code=404,
            detail="Translation not found",
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


# ---------------------------------------------------------------------------------------------------- #


@router.get("/work_analysis/meta/{meta_id}")
def get_work_analysis_meta_by_id(
    meta_id: int,
    user: User = Depends(CustomSecurity()),
):
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
def get_work_analysis_meta_by_work_analysis_id(
    work_analysis_id: UUID,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        meta = work_analysis_service.get_work_analysis_meta_by_work_analysis_id(
            conn, work_analysis_id
        )
        return meta


@router.post("/work_analysis/meta")
def create_work_analysis_meta(
    meta: WorkAnalysisMetaCreate,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            work_analysis_service.create_work_analysis_meta(conn, meta)

    except WorkAnalysisMetaKeyAlreadyExist:
        raise HTTPException(
            status_code=400,
            detail="Meta key already exist",
        )


@router.put("/work_analysis/meta/{meta_id}")
def update_work_analysis_meta(
    meta_id: int,
    meta: WorkAnalysisMetaCreate,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            work_analysis_service.update_work_analysis_meta(conn, meta_id, meta)

    except WorkAnalysisMetaNotFound:
        raise HTTPException(
            status_code=404,
            detail="Work Analysis meta not found",
        )


@router.delete("/work_analysis/meta/{meta_id}")
def delete_work_analysis_meta(
    meta_id: int,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            work_analysis_service.delete_work_analysis_meta(conn, meta_id)

    except WorkAnalysisMetaNotFound:
        raise HTTPException(
            status_code=404,
            detail="Work Analysis meta not found",
        )
