import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.utils.env import settings
from src.database.db_engine import metadata, engine
from src.database.db_engine_log import metadata_log, engine_log

# TODO: Remove when better structure
from src.database.tables import (
    annotation,
    biography,
    image,
    masterclass,
    partition,
    subtitle,
    tag,
    timecode,
    video,
    work_analysis
)
from src.users.models import user_table
from src.academies.models import academy_table
from src.comments.models import comment_table
# from src.router.router import routing #TODO TEMPORARY
# from utils.meilisearch import search #TODO TEMPORARY

origins = []
if settings.environment == "dev":
    frontend_port = os.getenv("FRONTEND_PORT", "")
    origins.extend(["http://localhost:" + frontend_port, "localhost:" + frontend_port])
else:
    pass
    # Todo, add dns of the frontend

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

# search('Mad')
from src.users.router import router as user_router
from src.authentification.router import router as auth_router

app.include_router(user_router)
app.include_router(auth_router)

metadata_log.create_all(bind=engine_log)
metadata.create_all(engine)

#TODO Remove when tests are set up or when can generate clean data
from src.utils.fake_data import generate_data
generate_data()

#TODO Gestion des roles d'authentification
# Endpoint accès seloon ton role de base/role masterclass
# Définir tt les roles

#primary_role admin user
#secondary_role 