from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from routers import index
from database.db_engine import engine

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

app.include_router(index.router)