import uuid
from datetime import datetime
from pydantic import BaseModel, Field

# What data we require from the user
class IssueCreate(BaseModel):
    title: str = Field(..., max_length=255, examples=["Database connection timeout"])
    description: str = Field(..., examples=["I encountered an internal server error when saving records..."])

# What data we return to the user
class IssueResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    reported_at: datetime

    class Config:
        from_attributes = True  # Allows Pydantic to read SQLAlchemy models