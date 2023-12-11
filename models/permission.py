from typing import List
from pydantic import BaseModel

class permission(BaseModel):
    id: str
    permissionName: str
    role: int
