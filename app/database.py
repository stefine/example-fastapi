# import psycopg2
# import time
# from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@" \
                          f"{settings.database_hostname}:{settings.database_port}/{settings.database_name}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(host="localhost", password="wss19881116",
#                                 database="fastapi", user="postgres", cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was sucessfully")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)
