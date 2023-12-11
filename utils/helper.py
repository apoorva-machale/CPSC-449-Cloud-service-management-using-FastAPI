def individual_permisssion(permission):
    return {
        "id":(str(permission["_id"])),
        "permission_name": (str(permission["permissionName"])),
        "role":str(permission["role"])

    }

def list_permissions(permisssions) -> list:
    return [individual_permisssion(permission) for permission in permisssions]
