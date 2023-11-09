from sqlalchemy import Column, String, DateTime, Integer, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UIObject(Base):
    """Definition of UI Objects"""
    __tablename__ = 'uiobjects'
    Id = Column(String, primary_key=True)
    Reference = Column(String)
    ParentRef = Column(String)
    Name = Column(String)
    Type = Column(String)
    Created = Column(DateTime)
    FilePath = Column(String)
    LibraryName = Column(String) # = UIReference
    __table_args__ = (UniqueConstraint('Reference', 'ParentRef', 'LibraryName'),)

class UIReference(Base):
    """References of UI Objects inside Process or library"""
    __tablename__ = 'uireferences'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Reference = Column(String) # = UIObject.Reference
    ActivityType = Column(String)
    DisplayName = Column(String)
    FilePath = Column(String)
    ProcessName = Column(String)
    __table_args__ = (UniqueConstraint('DisplayName', 'Reference', 'FilePath'),)

class Activity(Base):
    """Library Activities = Workflow names of Libraries"""
    __tablename__ = 'activities'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    LibraryName = Column(String)
    Name = Column(String)
    Type = Column(String)
    FilePath = Column(String)
    __table_args__ = (UniqueConstraint('Name', 'LibraryName'),)

class ActivityReference(Base):
    """References ("Invokes") of compiled library activities inside a Process (or library)"""
    __tablename__ = 'activityreferences'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    ProcessName = Column(String)
    ActivityName = Column(String)
    DisplayName = Column(String)
    Assembly = Column(String) # Assembly = Activity.LibraryName
    FilePath = Column(String)
    __table_args__ = (UniqueConstraint('ActivityName', 'ProcessName', 'FilePath'),)



