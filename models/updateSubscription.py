from pydantic import BaseModel, Field

class UpdateUserSubscription(BaseModel):
    subscription_plan_id: str = Field(..., description="The ID of the new subscription plan")