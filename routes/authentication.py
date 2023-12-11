
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from utils.authentication import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
from models.authentication import Token
from config.database import user_collection,permission_collection
from datetime import timedelta
from utils.helper import list_permissions

router = APIRouter(tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    print("In authenticate user function")
    user = user_collection.find_one({"username": username})
    print("USer find",user)
    if not user:
        return False

    if not verify_password(password, user["hashed_password"]):
        return False
    return user

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Getting the list of permissions for a given user as per role 
    # Encode permission in role
    print("User role is",user["role"])
    permissions = permission_collection.find({"role":user["role"]})
    permissions = list_permissions(permissions)
    print("Permsiions",permissions)
    user_permissions = [per["permission_name"] for per in permissions]
    access_token = create_access_token(
        data={"sub": user["username"],"role":user["role"],"permissions":user_permissions}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

    
#     user = authenticate_user(username, password)
#     print("Output offff uSer",user)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     # Getting the list of permissions for a given user as per role 
#     # Encode permission in role
#     print("User role is",user["role"])
#     permissions = permission_collection.find({"role":user["role"]})
#     permissions = list_permissions(permissions)
#     print("Permsiions",permissions)
#     user_permissions = [per["permission_name"] for per in permissions]
#     access_token = create_access_token(
#         data={"sub": user["username"],"role":user["role"],"permissions":user_permissions}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}



