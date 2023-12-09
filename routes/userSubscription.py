
from fastapi import APIRouter, HTTPException, status, Path, Body, Depends
from bson import ObjectId
from config.database import user_collection, subscription_collection
from utils.authentication import get_current_user
from models.updateSubscription import UpdateUserSubscription
from models.user import UserResponse
router = APIRouter()

@router.post("/users/{user_id}/subscribe")
async def update_user_subscription(
    user_id: str,
    subscription_update: UpdateUserSubscription,  # Renamed for clarity
    current_user: str = Depends(get_current_user)  # Require authentication
):
    # Verify that the current user is the one making the request or has permission
    if current_user != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this user's subscription")

    # Extract the subscription_plan_id from the request body
    subscription_plan_id = subscription_update.subscription_plan_id

    
    if not ObjectId.is_valid(subscription_plan_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid plan ID ")

    subscription_plan = subscription_collection.find_one({"_id": ObjectId(subscription_plan_id)})
    if not subscription_plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription plan not found")

    updated_user = user_collection.find_one_and_update(
        {"username": user_id},
        {"$set": {"subscriptionPlanId": ObjectId(subscription_plan_id)}},
        return_document=True
    )
    updated_user_dict = updated_user.to_dict() if hasattr(updated_user, "to_dict") else updated_user
    # Convert ObjectId fields to strings
    updated_user_dict["_id"] = str(updated_user_dict["_id"])
    updated_user_dict["subscriptionPlanId"] = str(subscription_plan_id)

    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "Subscription updated successfully", "user": updated_user}

@router.get("/users/{username}", response_model=UserResponse)
async def get_user_by_username(
    username: str,
    current_user: str = Depends(get_current_user)  # Include authentication
):
    if current_user != username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this user's information"
        )
    
    user = user_collection.find_one({"username": username})
    print (user)
    if user:
        # Convert the _id field to a string
        user['id'] = str(user['_id'])
        user['subscriptionPlanId'] = str(user['subscriptionPlanId'])
        # Create a UserResponse object, excluding sensitive fields like hashed_password
        return UserResponse(
            username=user['username'],
            email=user['email'],
            role=user['role'],
            subscription_plan_id=user['subscriptionPlanId']
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username '{username}' not found"
        )