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


class ActivitySchema(BaseModel):
    Reference: str
    ActivityType: str
    DisplayName: str
    FilePath: str
