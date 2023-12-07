def serialize_api_permission(permission: APIPermission) -> dict:
    return {
        "apiName": permission.apiName,
        "endpoint": permission.endpoint,
        "maxUsageLimit": permission.maxUsageLimit,
    }

def serialize_subscription_plan(plan: SubscriptionPlan) -> dict:
    return {
        "name": plan.name,
        "description": plan.description,
        "price": plan.price,
        "validityPeriod": plan.validityPeriod,
        "apiPermissions": [serialize_api_permission(perm) for perm in plan.apiPermissions],
    }
