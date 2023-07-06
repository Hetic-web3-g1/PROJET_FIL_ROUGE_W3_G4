from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings

# from utils.meilisearch import search

origins = []
if settings.environment in {"dev", "development"}:
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

app.include_router(user_router)
app.include_router(auth_router)
