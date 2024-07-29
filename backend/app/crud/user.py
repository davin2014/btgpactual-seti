from typing import Optional
from pymongo.errors import DuplicateKeyError, PyMongoError
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.user import UserCreate, UserInDB, UserUpdate, User
from app.core.security import get_password_hash
from app.db.db import  user_collection

async def get_user_by_email( email: str) -> Optional[User]:
    try:
        user_data = await user_collection.find_one({"email": email})
        if user_data:
            return User(**user_data)
        return None
    except PyMongoError as e:
        raise RuntimeError(f"Database error while retrieving user with email '{email}': {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error while retrieving user with email '{email}': {str(e)}")

async def create_user(user: UserCreate) -> Optional[UserInDB]:
    try:
        existing_user = await user_collection.find_one({"email": user.email})
        if existing_user:
            raise ValueError("A user with this email already exists.")

        hashed_password = get_password_hash(user.password)

        user_in_db = UserInDB(**user.model_dump(), hashed_password=hashed_password)

        await user_collection.insert_one(user_in_db.model_dump())

        return user_in_db
    except DuplicateKeyError:
        raise ValueError("A user with this email already exists.")
    except Exception as e:
        raise RuntimeError(f"Error creating user: {str(e)}")

async def update_user(user_id: str, user_update: UserUpdate) -> Optional[UserInDB]:
    try:
        existing_user = await user_collection.find_one({"_id": user_id})
        if not existing_user:
            raise ValueError("User not found.")

        update_data = user_update.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        result = await user_collection.update_one({"_id": user_id}, {"$set": update_data})
        if result.modified_count == 1:
            return await user_collection.find_one({"_id": user_id})
        return None
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error updating user: {str(e)}")
    

async def update_password(user_id: str, password: str) -> Optional[UserInDB]:
    try:
        hashed_password = get_password_hash(password)
        result = await user_collection.update_one({"_id": user_id}, {"$set": {"hashed_password": hashed_password}})
        if result.modified_count == 1:
            return await user_collection.find_one({"_id": user_id})
        return None
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error updating password: {str(e)}")