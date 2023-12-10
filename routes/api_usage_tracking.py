from fastapi import APIRouter, Depends, HTTPException, status
from config.database import user_collection, subscription_collection
# from utils.authentication import get_current_user
from bson import ObjectId

router = APIRouter()

@router.post("/trackUsage/{user_id}/{endpoint}")
async def track_api_usage(
    user_id: str,
    endpoint: str,
    # current_user: str = Depends(get_current_user)
):
    # Check if the current user is the one making the request
    # if current_user != user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not authorized to track usage for this user",
    #     )

    # Retrieve the user's subscription plan
    user_subscription = user_collection.find_one({"username": user_id})
    if not user_subscription or not user_subscription["subscriptionPlanId"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has no active subscription plan",
        )

    # Retrieve the subscription plan
    subscription_plan_id = user_subscription["subscriptionPlanId"]
    subscription_plan = subscription_collection.find_one({"_id": ObjectId(subscription_plan_id)})
    if not subscription_plan:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Subscription plan not found",
        )

    # Find the API permission in the subscription plan
    api_permission = next(
        (perm for perm in subscription_plan["apiPermissions"] if perm["endpoint"] == endpoint),
        None,
    )
    if not api_permission:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"API permission not found for endpoint: {endpoint}",
        )

    # Check if the user has reached the maximum limit
    if api_permission["maxUsageLimit"] <= subscription_plan.get("currentUsage", 0):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User has reached the maximum usage limit for endpoint: {endpoint}",
        )

    # Increment the current usage
    subscription_collection.update_one(
        {"_id": ObjectId(subscription_plan_id)},
        {"$inc": {"currentUsage": 1}},
    )

    return {"message": "API usage tracked successfully"}

@router.get("/usageLimitStatus/{user_id}/{endpoint}")
async def check_usage_limit_status(
    user_id: str,
    endpoint: str,
    # current_user: str = Depends(get_current_user)
):
    # Check if the current user is the one making the request
    # if current_user != user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not authorized to check usage limit status for this user",
    #     )

    # Retrieve the user's subscription plan
    user_subscription = user_collection.find_one({"username": user_id})
    if not user_subscription or not user_subscription["subscriptionPlanId"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has no active subscription plan",
        )

    # Retrieve the subscription plan
    subscription_plan_id = user_subscription["subscriptionPlanId"]
    subscription_plan = subscription_collection.find_one({"_id": ObjectId(subscription_plan_id)})
    if not subscription_plan:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Subscription plan not found",
        )

    # Find the API permission in the subscription plan
    api_permission = next(
        (perm for perm in subscription_plan["apiPermissions"] if perm["endpoint"] == endpoint),
        None,
    )
    if not api_permission:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"API permission not found for endpoint: {endpoint}",
        )

    return {
        "currentUsage": subscription_plan.get("currentUsage", 0),
        "maxUsageLimit": api_permission["maxUsageLimit"],
        "isWithinLimit": subscription_plan.get("currentUsage", 0) < api_permission["maxUsageLimit"],
    }
