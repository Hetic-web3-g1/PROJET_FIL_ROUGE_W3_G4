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
    partition,
    subtitle,
    tag,
    timecode,
    video,
    work_analysis
)
from src.users.models import user_table
from src.academies.models import academy_table
from src.masterclasses.models import (
    masterclass_table,
    masterclass_user_table,
    masterclass_video_table,
    masterclass_image_table,
    masterclass_comment_table,
    masterclass_tag_table
)
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
# from src.utils.fake_data import generate_data
# generate_data()
# import uuid

# from src.users.service import get_user_by_id, is_admin, has_masterclass_role
# from src.database.db_engine import engine
# with engine.connect() as conn:
#     user = get_user_by_id(conn, uuid.UUID("730abc71-6009-4cac-b946-dcf8b75a60e0"))
#     print(user)
#     print(is_admin(user))
#     id_user = uuid.UUID("12345648-1234-1234-1234-123456789123")
#     id_masterclass = uuid.UUID("0b30a97e-ce9c-4271-aeb7-ba7b138384da")
#     print(has_masterclass_role(conn, "teacher", id_user, id_masterclass))
#     print(has_masterclass_role(conn, "teachUJer", id_user, id_masterclass))