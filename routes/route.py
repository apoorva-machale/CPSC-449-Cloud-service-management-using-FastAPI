from fastapi import APIRouter
from models.subscriptionPlan import SubscriptionPlan, serialize_subscription_plan
from config.database import collection_name
from schema.schemas import list_serial
from bson import ObjectId

router = APIRouter()

@router.get("/subscriptionpPlans")
async def get_subscription_plan():
    subscription_plans=list_serial(collection_name.find())
    return subscription_plans


@router.post("/addSubscriptionPlans")
async def post_subscription_plan(subscription: SubscriptionPlan):
    collection_name.insert_one(serialize_subscription_plan(subscription))

@router.put("/updateSubscriptionPlan/{id}")
async def update_subscription_plan(id:str, subscription: SubscriptionPlan):
    collection_name.find_one_and_update({"_id": ObjectId(id)}, {"$set": serialize_subscription_plan(subscription)})

@router.delete("/deleteSubscriptionPlan/{id}")
async def delete_subscription_plan(id:str):
    collection_name.find_one_and_delete({"_id": ObjectId(id)})