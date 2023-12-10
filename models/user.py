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
    userCreated: Optional[bool] = None  
    subscription_plan_id: Optional[str] = None

# class UserStatistics(BaseModel):
#     user_id: str
#     total_requests: int
#     successful_requests: int
#     failed_requests: int

class UserStatistics(BaseModel):
    user_name: str
    total_requests: int
    successful_requests: int
    failed_requests: int