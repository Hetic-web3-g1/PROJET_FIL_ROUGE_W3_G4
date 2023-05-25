from fastapi import APIRouter

router = APIRouter(
    prefix="",
    tags=["index"],
)

@router.get("/")
def read_root():
    return {"msg": "Hello World"}