from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UIObject(Base):
    __tablename__ = 'uiobjects'

    Id = Column(String, primary_key=True)
    Reference = Column(String)
    ParentRef = Column(String)
    Name = Column(String)
    Type = Column(String)
    Created = Column(DateTime)
    FilePath = Column(String)

class Activity(Base):
    __tablename__ = 'activities'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Reference = Column(String)
    ActivityType = Column(String)
    DisplayName = Column(String)
    FilePath = Column(String)

