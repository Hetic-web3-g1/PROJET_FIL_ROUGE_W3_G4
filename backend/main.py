from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from src.middleware.log_error import LogErrorMiddleware
from src.utils.fake_data import generate_data

if settings.environment in {"development"}:
    origins = ["*"]
else:
    origins = ["groupe4.hetic-projects.arcplex.tech:80"]

app = FastAPI()
api = FastAPI(root_path="/api")
api_public = FastAPI(root_path="/api-public")

app.mount("/api", app=api)
app.mount("/api-public", app=api_public)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
)

app.add_middleware(LogErrorMiddleware)

from src.entities.academies.router import router as academy_router
from src.entities.annotations.router import router as annotation_router
from src.entities.authentification.router import router as auth_router
from src.entities.biographies.router import router as biography_router
from src.entities.comments.router import router as comment_router
from src.entities.images.router import router as image_router
from src.entities.masterclasses.router import router as masterclass_router
from src.entities.partitions.router import router as partition_router
from src.entities.s3_objects.router import router as s3_object_router
from src.entities.subtitles.router import router as subtitle_router
from src.entities.tags.router import router as tag_router
from src.entities.users.router import router as user_router
from src.entities.videos.router import router as video_router
from src.entities.work_analyses.router import router as work_analysis_router

api.include_router(academy_router)
api.include_router(annotation_router)
api.include_router(auth_router)
api.include_router(biography_router)
api.include_router(comment_router)
api.include_router(masterclass_router)
api.include_router(image_router)
api.include_router(partition_router)
api.include_router(s3_object_router)
api.include_router(subtitle_router)
api.include_router(user_router)
api.include_router(tag_router)
api.include_router(video_router)
api.include_router(work_analysis_router)


from src.entities.annotations.router_public import router as annotation_router_public
from src.entities.biographies.router_public import router as biography_router_public
from src.entities.images.router_public import router as image_router_public
from src.entities.masterclasses.router_public import (
    router as masterclass_router_public,
)
from src.entities.partitions.router_public import router as partition_router_public
from src.entities.s3_objects.router_public import router as s3_object_router_public
from src.entities.subtitles.router_public import router as subtitle_router_public
from src.entities.tags.router_public import router as tag_router_public
from src.entities.videos.router_public import router as video_router_public
from src.entities.work_analyses.router_public import (
    router as work_analysis_router_public,
)

api_public.include_router(annotation_router_public)
api_public.include_router(biography_router_public)
api_public.include_router(image_router_public)
api_public.include_router(masterclass_router_public)
api_public.include_router(partition_router_public)
api_public.include_router(s3_object_router_public)
api_public.include_router(subtitle_router_public)
api_public.include_router(tag_router_public)
api_public.include_router(video_router_public)
api_public.include_router(work_analysis_router_public)

# generate_data()
