from fastapi import APIRouter

router = APIRouter(
    prefix="/public",
    tags=["public"],
)


@router.get("/hello")
def hello():
    return {"message": "Hello World I'm the public API"}
