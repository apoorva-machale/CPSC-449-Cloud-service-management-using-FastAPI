
from fastapi import APIRouter, HTTPException, status, Path, Body, Depends
from bson import ObjectId
from config.database import user_collection, subscription_collection,collection_user_statistics
from utils.authentication import get_current_user
from models.updateSubscription import UpdateUserSubscription
from models.user import UserResponse,UserStatistics
router = APIRouter()

from models.user import UserResponse
from utils.authentication import validate_permission

from fastapi.security import HTTPBearer


security = HTTPBearer()
router = APIRouter(tags=["UserSubscription"])

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
    
@router.get("/mySubscription/{userName}")
async def get_user_subscription(
    userName: str,
    current_user: str = Depends(get_current_user)
):
    if current_user!=userName:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view subscription"
        )
    userDetails = user_collection.find_one({"username": userName})
    if userDetails:
        subcriptionPlanId = userDetails["subscriptionPlanId"]
        if subcriptionPlanId:
            subscriptionDetails = subscription_collection.find_one({"_id": ObjectId(subcriptionPlanId)})
            if subscriptionDetails:
                return {
                    "subscriptionName": subscriptionDetails["name"],
                    "description": subscriptionDetails["description"],
                    "price": subscriptionDetails["price"],
                    "validityPeriod": subscriptionDetails["validityPeriod"],
                    "apiPermissions": subscriptionDetails["apiPermissions"]
                }
            else:
                  raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Subscription details not found"
                        )
        else:
            raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"No associated Subscriptions"
                        )
    else:
        raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User details not found"
                        )
    


# Update customer's subscription plan
@router.put("/users/{username}/modify-subscription", response_model=UserResponse)
async def modify_subscription_plan(
    username: str,
    subscription_update: UpdateUserSubscription,
    current_user: str = Depends(get_current_user)
):
    
        # Verify that the current user is the one making the request or has permission
        if current_user != username:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify subscription plan")

        # Extract the subscription_plan_id from the request body
        subscription_plan_id = subscription_update.subscription_plan_id

        if not ObjectId.is_valid(subscription_plan_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid plan ID")

        # Check if the subscription plan exists
        subscription_plan = subscription_collection.find_one({"_id": ObjectId(subscription_plan_id)})
        if not subscription_plan:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription plan not found")

        # Update user's subscription plan
        updated_user = user_collection.find_one_and_update(
            {"username": username},
            {"$set": {"subscriptionPlanId": ObjectId(subscription_plan_id)}},
            return_document=True
        )

        if not updated_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Convert ObjectId fields to strings
        updated_user_dict = updated_user.to_dict() if hasattr(updated_user, "to_dict") else updated_user
        updated_user_dict["_id"] = str(updated_user_dict["_id"])
        updated_user_dict["subscriptionPlanId"] = str(subscription_plan_id)

        message = "Subscription plan updated successfully"

        # Create a UserResponse object, excluding sensitive fields like hashed_password
        return UserResponse(
            
            username=updated_user_dict['username'],
            email=updated_user_dict['email'],
            role=updated_user_dict['role'],
            subscription_plan_id=updated_user_dict['subscriptionPlanId']
        )

#Insert user statistics
@router.post("/user_statistics", response_model=UserStatistics)
async def insert_user_statistics(user_statistics: UserStatistics):
    try:
        result = collection_user_statistics.insert_one(user_statistics.dict())
        if result.inserted_id is None:
            raise HTTPException(status_code=500, detail="Failed to insert user statistics")

        return user_statistics

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Access user statistics    

@router.get("/user_statistics_by_name/{user_name}", response_model=UserStatistics)
def get_user_statistics_by_name(user_name: str):
    try:
        user_statistics = collection_user_statistics.find_one({"user_name": user_name})
        if not user_statistics:
            raise HTTPException(status_code=404, detail="User statistics not found")

        return UserStatistics(**user_statistics)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





    