from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class Role(str, Enum):
    admin = "admin"
    customer = "customer"

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    role: Role = Role.customer

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserInDB(UserBase):
    id: Optional[str] = None
    hashed_password: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "role": "customer",
            }
        }
        exclude = {"hashed_password"}

class UserResponse(BaseModel):
    id: Optional[str] = None
    username: str
    email: str
    role: Role
    userCreated: bool