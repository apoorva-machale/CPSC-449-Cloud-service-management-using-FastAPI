from typing import List
from pydantic import BaseModel

class APIPermission(BaseModel):
    apiName: str 
    endpoint: str
    maxUsageLimit: int


class SubscriptionPlan(BaseModel):
    id: str
    name: str
    description: str
    price: float
    validityPeriod: str
    apiPermissions: List[APIPermission]

# Function to serialize APIPermission objects to dictionaries
def serialize_api_permission(permission: APIPermission) -> dict:
    return {
        "apiName": permission.apiName,
        "endpoint": permission.endpoint,
        "maxUsageLimit": permission.maxUsageLimit,
    }

# Function to serialize a SubscriptionPlan object to a dictionary
def serialize_subscription_plan(plan: SubscriptionPlan) -> dict:
    return {
        "name": plan.name,
        "description": plan.description,
        "price": plan.price,
        "validityPeriod": plan.validityPeriod,
        "apiPermissions": [serialize_api_permission(perm) for perm in plan.apiPermissions],
    }

