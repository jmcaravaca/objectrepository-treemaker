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
    Type: str #TestCase or Activity or ProcessWorkflow
    FilePath: str

class ActivityReferenceSchema(BaseModel):
    ProcessName: str
    ActivityName: str
    DisplayName: str
    Assembly: str
    FilePath: str

class ConfigSchema(BaseModel):
    ProcessName: str
    Name: str
    Sheet: str #TestCase or Activity or ProcessWorkflow
    Value: str #TestCase or Activity or ProcessWorkflow
    FilePath: str
    
class ConfigReferenceSchema(BaseModel):
    ProcessName: str
    WorkflowName: str
    KeyReference: str
    FilePath: str    