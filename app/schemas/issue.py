import uuid
from datetime import datetime
from pydantic import BaseModel, Field

class IssueResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    reported_at: datetime

    class Config:
        from_attributes = True  # Allows Pydantic to read SQLAlchemy models

class IssueCreate(BaseModel):
    title: str = Field(..., max_length=255, examples=["Database connection timeout"])
    description: str = Field(..., examples=["I encountered an internal server error when saving records..."])

class IssueDelete(BaseModel):
    id: uuid.UUID

class IssueEdit(BaseModel):
    id: uuid.UUID
    title: str = Field(..., max_length=255, examples={"Database connection timeout"})
    description: str = Field(..., examples="I encountered an internal server error when saving records...")