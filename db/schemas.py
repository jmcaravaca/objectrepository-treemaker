from pydantic import BaseModel
from datetime import datetime

class UIObjectSchema(BaseModel):
    Id: str
    Reference: str
    ParentRef: str
    Name: str
    Type: str
    Created: datetime
    FilePath: str
    LibraryName: str

class UIReferenceSchema(BaseModel):
    Reference: str
    ActivityType: str
    DisplayName: str
    FilePath: str
    ProcessName: str

class ActivitySchema(BaseModel):
    LibraryName: str
    Name: str
    FilePath: str

class ActivityReferenceSchema(BaseModel):
    ProcessName: str
    ActivityName: str
    DisplayName: str
    Assembly: str
    FilePath: str
