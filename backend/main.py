from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings

from src.utils.fake_data import generate_data

origins = []

if settings.environment in {"development"}:
    origins = ["*"]
else:
    pass
    # Todo: production, add dns of the frontend

app = FastAPI(
    # root_path="/api"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from src.entities.academies.router import router as academy_router
from src.entities.authentification.router import router as auth_router
from src.entities.biographies.router import router as biography_router
from src.entities.masterclasses.router import router as masterclass_router
from src.entities.partitions.router import router as partition_router
from src.entities.users.router import router as user_router
from src.entities.tags.router import router as tag_router
from src.entities.work_analyses.router import router as work_analysis_router

app.include_router(academy_router)
app.include_router(auth_router)
app.include_router(biography_router)
app.include_router(masterclass_router)
app.include_router(partition_router)
app.include_router(user_router)
app.include_router(tag_router)
app.include_router(work_analysis_router)

# Todo: remove when have clean data
generate_data()
