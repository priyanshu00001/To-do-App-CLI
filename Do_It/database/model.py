from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()


class Task(Base):
    __tablename__ = "Tasks"
    taskId = Column(Integer, autoincrement=True, primary_key=True)
    task = Column(String)
    time = Column(DateTime)
    is_done = Column(Boolean, default=False)


engine = create_engine("sqlite:///database/tasks.db")
session = Session(engine)
