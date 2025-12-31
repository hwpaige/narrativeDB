from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, BigInteger, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class Launch(Base):
    __tablename__ = 'launches'

    id = Column(Integer, primary_key=True)
    cospar_id = Column(String)
    sort_date = Column(BigInteger)
    name = Column(String)
    provider = Column(JSON)
    vehicle = Column(String)
    pad = Column(JSON)
    location = Column(JSON)
    agencies = Column(JSON)
    mission = Column(JSON)
    mission_type = Column(String)
    orbit = Column(JSON)
    launch_description = Column(Text)
    win_open = Column(DateTime)
    t0 = Column(DateTime)
    win_close = Column(DateTime)
    est_date = Column(JSON)
    date_str = Column(String)
    tags = Column(JSON)
    slug = Column(String)
    media = Column(JSON)
    result = Column(Integer)
    suborbital = Column(Boolean)
    modified = Column(DateTime)
    type = Column(String)  # 'upcoming' or 'past'

# Database setup
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///launches.db')  # Default to SQLite for local dev
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
