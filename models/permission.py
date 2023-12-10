from pydantic import BaseModel

class Permission(BaseModel):
    id: str
    name: str
    apiId: str
    description: str
    endpoint: str