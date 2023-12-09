from fastapi import APIRouter, HTTPException, status, Body
from models.user import UserCreate, UserResponse
from config.database import user_collection
from bson import ObjectId
from passlib.context import CryptContext
from pymongo.errors import DuplicateKeyError

router = APIRouter()

# Password context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Register user endpoint
@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
     # Check for existing user with the same username or email
    if user_collection.find_one({"username": user.username}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    if user_collection.find_one({"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    # Hash the user's password
    hashed_password = pwd_context.hash(user.password)
    # Create a new user object with hashed password
    user_in_db = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "role": user.role.value
    }
     # Save the new user to the database
    try:
        result = user_collection.insert_one(user_in_db)
        user_in_db['id'] = str(result.inserted_id)
        return UserResponse(
            id=user_in_db['id'],
            username=user_in_db['username'],
            email=user_in_db['email'],
            role=user_in_db['role'],
            userCreated=True
        )
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User could not be created"
        )