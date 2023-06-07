from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pip import main
import os

from sqlalchemy.ext.asyncio import create_async_engine

from database.db_engine import metadata, engine
from database.tables import academy, annotation, biography, comment, image, masterclass, partition, subtitle, tag, timecode, user, video, work_analysis
from utils.fake_data import generate_data
from router.router import routing
# from utils.meilisearch import search

metadata.create_all(bind=engine)

frontend_port = os.getenv('FRONTEND_PORT')
origins = [
    "http://localhost:" + frontend_port,
    "localhost:" + frontend_port
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# search('Mad')

routing(app)
