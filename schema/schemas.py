def individual_serial(subscription_plan) -> dict:
    return {
        "id": str(subscription_plan["_id"]),
        "name": subscription_plan["name"],
        "description": subscription_plan["description"],
        "price": subscription_plan["price"],
        "validityPeriod": subscription_plan["validityPeriod"],
        "apiPermissions": [
            {
                "apiName": permission["apiName"],
                "endpoint": permission["endpoint"],
                "maxUsageLimit": permission["maxUsageLimit"]
            } for permission in subscription_plan.get("apiPermissions", [])
        ]
    }

def list_serial(subscription_plans) -> list:
    return [individual_serial(subscription_plan) for subscription_plan in subscription_plans]
