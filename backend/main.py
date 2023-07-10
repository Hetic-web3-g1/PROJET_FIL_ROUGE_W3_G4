from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings

# from utils.meilisearch import search
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

from src.users.router import router as user_router
from src.authentification.router import router as auth_router
from src.masterclasses.router import router as masterclass_router
from src.biographies.router import router as biography_router
from src.partitions.router import router as partition_router

app.include_router(user_router)
app.include_router(auth_router)

app.include_router(masterclass_router)
app.include_router(biography_router)
app.include_router(partition_router)

generate_data()
