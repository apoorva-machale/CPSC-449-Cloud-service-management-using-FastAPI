from fastapi import Request, Depends, HTTPException, status
from config.database import user_collection, subscription_collection
from utils.authentication import get_current_user

async def get_api_endpoint(request: Request):
    return request.url.path

def get_base_api_endpoint(api_endpoint: str):
    # Split the endpoint and return the base part (e.g., '/weather')
    return '/' + api_endpoint.split('/')[1]

async def get_user_subscription_plan(username: str):
    # Retrieve user document from the database
    user = user_collection.find_one({"username": username})
    if not user:
        return None
    
    if not user["subscriptionPlanId"]:
        return None

    # Retrieve the subscription plan using the subscriptionPlanId from the user document
    subscription_plan = subscription_collection.find_one({"_id": user["subscriptionPlanId"]})
    if not subscription_plan:
        return None
    return subscription_plan


async def check_api_permission(
    current_user: str = Depends(get_current_user),
    api_endpoint: str = Depends(get_api_endpoint)
):
    base_api_endpoint = get_base_api_endpoint(api_endpoint)
    subscription_plan = await get_user_subscription_plan(current_user)
    print(subscription_plan)
    print (api_endpoint)
    print(current_user)
    if subscription_plan:
        # Check if the API endpoint is in the user's subscription plan
        for permission in subscription_plan["apiPermissions"]:
            print(permission["endpoint"])
            if get_base_api_endpoint(permission["endpoint"]) == base_api_endpoint:
                # Here you can also implement logic to check the usage limit
                return True

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access to this API is not allowed with your subscription plan."
    )
