from sqlalchemy import func, select
from faker import Faker
import random

from utils.log import logging
from database.db_engine import engine
from database.tables.academy import academy_table
from database.tables.biography import biography_table
from database.tables.comment import comment_table
from database.tables.masterclass import masterclass_table
from database.tables.partition import partition_table
from database.tables.tag import tag_table
from database.tables.user import user_table
from database.tables.video import video_table
from database.tables.work_analysis import work_analysis_table
from schema.academy import AcademyCreate
from schema.biography import BiographyCreate
from schema.comment import CommentCreate
from schema.masterclass import MasterclassCreate
from schema.partition import PartitionCreate
from schema.tag import TagCreate
from schema.user import UserCreate
from schema.video import VideoCreate
from schema.work_analysis import WorkAnalysisCreate
from manager.academy_manager import create_academy
from manager.biography_manager import create_biography
from manager.comment_manager import create_comment
from manager.masterclass_manager import create_masterclass
from manager.partition_manager import create_partition
from manager.tag_manager import create_tag
from manager.user_manager import create_user
from manager.video_manager import create_video
from manager.work_analysis_manager import create_work_analysis
from manager.fake_manager import create_fixed_user, create_fixed_academy

def create_academy_fake():
    with engine.begin() as conn:
        academy = AcademyCreate(**{
            "name": Faker().company()
        })
        create_academy(conn, academy)

def create_fixed_academy_fake():
    with engine.begin() as conn:
        academy = AcademyCreate(**{
            "name": "Saline Royale Academy"
        })
        create_fixed_academy(conn, academy)

def create_biography_fake():
    with engine.begin() as conn:
        roles = ["teacher", "compositor"]
        biography = BiographyCreate(**{
            "first_name": Faker().first_name(),
            "last_name": Faker().last_name(),
            "instrument": [Faker().word()],
            "nationality": Faker().country(),
            "website": Faker().url(),
            "award": [Faker().word()],
            "content": Faker().text(),
            "type": random.choice(roles),
            "status": "created",
            "created_by": "12345648-1234-1234-1234-123456789123"
        })
        create_biography(conn, biography)

def create_comment_fake():
    with engine.begin() as conn:
        comment = CommentCreate(**{
            "content": Faker().text(),
            "created_by": "12345648-1234-1234-1234-123456789123"
        })
        create_comment(conn, comment)

def create_masterclass_fake():
    with engine.begin() as conn:
        masterclass = MasterclassCreate(**{
            "academy_id": "12345648-1234-1234-1234-123456789123",
            "title": Faker().word(),
            "description": Faker().text(),
            "status": "created",
            "created_by": "12345648-1234-1234-1234-123456789123"
        })
        create_masterclass(conn, masterclass)

def create_partition_fake():
    with engine.begin() as conn:
        partition = PartitionCreate(**{
            "status": "created",
            "file_name": Faker().word(),
            "created_by": "12345648-1234-1234-1234-123456789123"
        })
        create_partition(conn, partition)

def create_tag_fake():
    with engine.begin() as conn:
        tag = TagCreate(**{
            "content": Faker().word()
        })
        create_tag(conn, tag)

def create_user_fake():
    with engine.begin() as conn:
        roles = ["user", "teacher", "admin"]
        user = UserCreate(**{
            "first_name": Faker().first_name(),
            "last_name": Faker().last_name(),
            "email": Faker().email(),
            "password": Faker().password(),
            "role": random.choice(roles),
            "academy_id" : Faker().uuid4()
        })
        create_user(conn, user)

def create_fixed_user_fake():
    with engine.begin() as conn:
        user = UserCreate(**{
            "first_name": "admin",
            "last_name": "admin",
            "email": "admin@admin.com",
            "password": "admin",
            "role": "admin",
            "academy_id": "12345648-1234-1234-1234-123456789123",
        })
        create_fixed_user(conn, user)      

def create_video_fake():
    with engine.begin() as conn:
        video = VideoCreate(**{
            "version": random.uniform(1.0, 10.0),
            "title": Faker().word(),
            "duration": random.uniform(60.0, 120.0),
            "status": "created",
            "file_name": Faker().word(),
            "created_by": "12345648-1234-1234-1234-123456789123"
        })
        create_video(conn, video)

def create_work_analyse_fake():
    with engine.begin() as conn:
        work_analysis = WorkAnalysisCreate(**{
            "about": Faker().text(),
            "learning":[Faker().word()],
            "content": Faker().text(),
            "status": "created",
            "created_by": "12345648-1234-1234-1234-123456789123"
        })
        create_work_analysis(conn, work_analysis)

def has_data(conn, table):
    result = conn.execute(select(func.count()).select_from(table)).scalar()
    return result > 0

def generate_data():
    tables = {
        academy_table: create_academy_fake,
        biography_table: create_biography_fake,
        comment_table: create_comment_fake,
        masterclass_table: create_masterclass_fake,
        partition_table: create_partition_fake,
        tag_table: create_tag_fake,
        user_table: create_user_fake,
        video_table: create_video_fake,
        work_analysis_table: create_work_analyse_fake
    }

    with engine.begin() as conn:
        for table, create_func in tables.items():
            if not has_data(conn, table):  # Check if table is empty
                logging.info(f"Generating data for {table.name}")
                if table == user_table:
                    create_fixed_user_fake()
                if table == academy_table:
                    create_fixed_academy_fake()
                for _ in range(10):
                    create_func()