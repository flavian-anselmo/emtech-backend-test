from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    full_name: str
    password: str
    role: str


class UserResponse(BaseModel):
    user_id: int
    username: str
    full_name: str
    role: str
    created_at: datetime

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    user_id: int



class TaskCreate(BaseModel):
    title: str
    description: str
    assigned_to: int

class TaskResponse(BaseModel):
    task_id: int
    title: str
    description: str
    status: str
    assigned_to: int
    created_by: int

    class Config:
        orm_mode = True

class TaskStatusUpdate(BaseModel):
    status: str


class TaskFileResponse(BaseModel):
    id: int
    filename: str
    filepath: str
    task_id: int

    class Config:
        orm_mode = True