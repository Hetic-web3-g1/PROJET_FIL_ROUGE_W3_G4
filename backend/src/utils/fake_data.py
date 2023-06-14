from sqlalchemy import func, select
from faker import Faker
import random
import uuid

from sqlalchemy.engine import Connection

from src.database import db_srv
from src.database.db_engine import engine
from src.academies.models import academy_table
from src.academies.schemas import AcademyCreate
from src.academies.service import create_academy
from src.users.models import user_table
from src.users.schemas import UserCreate
from src.users.service import create_user
from src.masterclasses.models import masterclass_table
from src.masterclasses.schemas import MasterclassCreate
from src.masterclasses.service import create_masterclass
from src.comments.models import comment_table
from src.comments.schemas import CommentCreate
from src.comments.service import create_comment

def create_academy_fake():
    with engine.begin() as conn:
        academy = AcademyCreate(**{
            "name": Faker().company()
        })
        create_academy(conn, academy)
  
def create_fixed_academy(conn: Connection, academy: AcademyCreate):
    return db_srv.create_object(conn, academy_table, academy.dict(), object_id="12345648-1234-1234-1234-123456789123")

def create_fixed_academy_fake():
    with engine.begin() as conn:
        academy = AcademyCreate(**{
            "name": "Saline Royale Academy"
        })
        create_fixed_academy(conn, academy)

# def create_annotation_fake():
#     with engine.begin() as conn:
#         annotation = AnnotationCreate(**{
#             "measure": random.randint(1, 100),
#             "content": Faker().text(),
#             "created_by": "12345648-1234-1234-1234-123456789123"
#         })
#         create_annotation(conn, annotation)

# def create_biography_fake():
#     with engine.begin() as conn:
#         roles = ["teacher", "compositor"]
#         biography = BiographyCreate(**{
#             "first_name": Faker().first_name(),
#             "last_name": Faker().last_name(),
#             "instrument": [Faker().word()],
#             "nationality": Faker().country(),
#             "website": Faker().url(),
#             "award": [Faker().word()],
#             "content": Faker().text(),
#             "type": random.choice(roles),
#             "status": "created",
#             "created_by": "12345648-1234-1234-1234-123456789123"
#         })
#         create_biography(conn, biography)

def create_comment_fake():
    with engine.begin() as conn:
        comment = CommentCreate(**{
            "content": Faker().text(),
        })
        create_comment(conn, comment, user_id=uuid.UUID("12345648-1234-1234-1234-123456789123"))

# def create_image_fake():
#     with engine.begin() as conn:
#         image = ImageCreate(**{
#             "title": Faker().word(),
#             "file_name": Faker().word(),
#             "created_by": "12345648-1234-1234-1234-123456789123"
#         })
#         create_image(conn, image)

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

# def create_partition_fake():
#     with engine.begin() as conn:
#         partition = PartitionCreate(**{
#             "status": "created",
#             "file_name": Faker().word(),
#             "created_by": "12345648-1234-1234-1234-123456789123"
#         })
#         create_partition(conn, partition)

# def create_tag_fake():
#     with engine.begin() as conn:
#         tag = TagCreate(**{
#             "content": Faker().word()
#         })
#         create_tag(conn, tag)

def create_user_fake():
    with engine.begin() as conn:
        roles = ["user", "teacher", "admin"]
        user = UserCreate(**{
            "first_name": Faker().first_name(),
            "last_name": Faker().last_name(),
            "email": Faker().email(),
            "password": Faker().password(),
            "role": random.choice(roles),
            "academy_id" : uuid.UUID("12345648-1234-1234-1234-123456789123")
        })
        create_user(conn, user)

def create_fixed_user(conn: Connection, user: UserCreate):
    return db_srv.create_object(conn, user_table, user.dict(), object_id="12345648-1234-1234-1234-123456789123")

def create_fixed_user_fake():
    with engine.begin() as conn:
        user = UserCreate(**{
            "first_name": "admin",
            "last_name": "admin",
            "email": "admin@admin.com",
            "password": "admin",
            "role": "admin",
            "academy_id": uuid.UUID("12345648-1234-1234-1234-123456789123")
        })
        create_fixed_user(conn, user)      

# def create_video_fake():
#     with engine.begin() as conn:
#         video = VideoCreate(**{
#             "version": random.uniform(1.0, 10.0),
#             "title": Faker().word(),
#             "duration": random.uniform(60.0, 120.0),
#             "status": "created",
#             "file_name": Faker().word(),
#             "created_by": "12345648-1234-1234-1234-123456789123"
#         })
#         create_video(conn, video)

# def create_work_analyse_fake():
#     with engine.begin() as conn:
#         work_analysis = WorkAnalysisCreate(**{
#             "about": Faker().text(),
#             "learning":[Faker().word()],
#             "content": Faker().text(),
#             "status": "created",
#             "created_by": "12345648-1234-1234-1234-123456789123"
#         })
#         create_work_analysis(conn, work_analysis)

def has_data(conn, table):
    result = conn.execute(select(func.count()).select_from(table)).scalar()
    return result > 0

def generate_data():
    tables = {
        academy_table: create_academy_fake,
        user_table: create_user_fake,
        # annotation_table: create_annotation_fake,
        # biography_table: create_biography_fake,
        comment_table: create_comment_fake,
        # image_table: create_image_fake,
        masterclass_table: create_masterclass_fake,
        # partition_table: create_partition_fake,
        # tag_table: create_tag_fake,
        # video_table: create_video_fake,
        # work_analysis_table: create_work_analyse_fake
    }
    
    with engine.begin() as conn:
        for table, create_func in tables.items():
            if not has_data(conn, table):  # Check if table is empty
                if table == academy_table:
                    create_fixed_academy_fake()
                if table == user_table:
                    create_fixed_user_fake()
                for _ in range(10):
                    create_func()