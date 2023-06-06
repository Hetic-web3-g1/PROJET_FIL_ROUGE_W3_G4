from fastapi import APIRouter

router = APIRouter(
    prefix="",
    tags=["Index"],
)

@router.get("/")
def read_root():
    return {"msg": "Hello World"}