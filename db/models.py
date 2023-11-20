from sqlalchemy import Column, String, DateTime, Integer, UniqueConstraint, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class UIObject(Base):
    """Definition of UI Objects"""

    __tablename__ = "uiobjects"
    Id = Column(String, primary_key=True)
    Reference = Column(String)
    ParentRef = Column(String)
    Name = Column(String)
    Type = Column(String)
    Created = Column(DateTime)
    FilePath = Column(String)
    LibraryName = Column(String)  # = UIReference
    __table_args__ = (UniqueConstraint("Reference", "ParentRef", "LibraryName"),)
    # Define the relationship from UIObject to UIReference
    references = relationship("UIReference", back_populates="ui_object")    


class UIReference(Base):
    """References of UI Objects inside Process or library"""

    __tablename__ = "uireferences"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Reference = Column(String, ForeignKey("uiobjects.Reference"))  # = UIObject.Reference
    ActivityType = Column(String)
    DisplayName = Column(String)
    FilePath = Column(String)
    ProcessName = Column(String)
    __table_args__ = (UniqueConstraint("DisplayName", "Reference", "FilePath"),)
    # Define the relationship from UIReference to UIObject
    ui_object = relationship("UIObject", back_populates="references")    


class Activity(Base):
    """Library Activities = Workflow names of Libraries"""

    __tablename__ = "activities"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    LibraryName = Column(String)
    Name = Column(String)
    Type = Column(String)
    FilePath = Column(String)
    __table_args__ = (UniqueConstraint("Name", "LibraryName"),)


class ActivityReference(Base):
    """References ("Invokes") of compiled library activities inside a Process (or library)"""

    __tablename__ = "activityreferences"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    ProcessName = Column(String)
    ActivityName = Column(String)
    DisplayName = Column(String)
    Assembly = Column(String)  # Assembly = Activity.LibraryName
    FilePath = Column(String)
    __table_args__ = (UniqueConstraint("ActivityName", "ProcessName", "FilePath"),)


class Config(Base):
    """KeyValues of Configs for processes"""

    __tablename__ = "configs"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    ProcessName = Column(String)
    Name = Column(String)
    Sheet = Column(String)
    Value = Column(String)  # Assembly = Activity.LibraryName
    FilePath = Column(String)
    __table_args__ = (UniqueConstraint("Name", "Sheet", "FilePath", "ProcessName"),)


class ConfigReference(Base):
    """References to Config values."""

    __tablename__ = "configreferences"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    ProcessName = Column(String)
    WorkflowName = Column(String)
    KeyReference = Column(String)
    FilePath = Column(String)
    __table_args__ = (UniqueConstraint("ProcessName", "WorkflowName", "KeyReference"),)
