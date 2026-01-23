import os
import sys
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()


class Task(Base):
    __tablename__ = "Tasks"
    taskId = Column(Integer, autoincrement=True, primary_key=True)
    task = Column(String)
    time = Column(DateTime)
    is_done = Column(Boolean, default=False)
    comment = Column(String, default="")


BASE_DIR = (
    os.path.dirname(sys.executable)
    if getattr(sys, "frozen", False)
    else os.path.dirname(os.path.abspath(__file__))
)

DB_PATH = os.path.join(BASE_DIR, "tasks.db")

engine = create_engine(f"sqlite:///{DB_PATH}")
session = Session(engine)


def createDb():
    Base.metadata.create_all(engine)
