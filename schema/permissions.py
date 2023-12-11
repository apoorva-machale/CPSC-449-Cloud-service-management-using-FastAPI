from pydantic import BaseModel



class CreatePermission(BaseModel):
    permissionName:str
    role:str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "permissionName": "create_subscription",
                    "role": "admin"
                }
            ]
        }
    }

class DeletePermission(BaseModel):
    permissionName:str
    role:str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "permissionName": "create_subscription",
                    "role": "admin"
                }
            ]
        }
    }