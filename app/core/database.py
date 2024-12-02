from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.settings import settings

databaseUrl = settings.database_url

engine = create_engine(databaseUrl)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def get_session():
    session= SessionLocal()
    try:
        yield session
    finally:
        session.close()