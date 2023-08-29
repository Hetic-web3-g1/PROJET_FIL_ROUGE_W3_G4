from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from src.utils.fake_data import generate_data

origins = ["*"]

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


from src.entities.academies.router import router as academy_router
from src.entities.annotations.router import router as annotation_router
from src.entities.authentification.router import router as auth_router
from src.entities.biographies.router import router as biography_router
from src.entities.comments.router import router as comment_router
from src.entities.masterclasses.router import router as masterclass_router
from src.entities.images.router import router as image_router
from src.entities.partitions.router import router as partition_router
from src.entities.public.router import router as public_router
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

api_public.include_router(public_router)


# Todo: remove when have clean data
generate_data()
