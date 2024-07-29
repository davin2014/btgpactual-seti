from fastapi import APIRouter, Depends, HTTPException
from app.models.user import UserCreate, UserUpdate, UserPublic, UpdatePassword, Message, UserInDB
from app.core.config import settings
from app.crud.user import get_user_by_email, create_user, update_user
from app.api.deps import get_current_active_superuser, get_current_user
from app.core.security import verify_password, get_password_hash
from app.db import db 

router = APIRouter()




@router.post("/", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic)
async def create_user(user_in: UserCreate):
    user = await get_user_by_email(user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="The user with this email already exists in the system.")
    user = await create_user(user_in)
    return user

@router.patch("/me", response_model=UserPublic)
async def update_user_me(user_in: UserUpdate, current_user: UserInDB = Depends(get_current_user)):
    if user_in.email:
        existing_user = await get_user_by_email(user_in.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(status_code=409, detail="User with this email already exists")
    user = await update_user(current_user.id, user_in)
    return user

@router.patch("/me/password", response_model=Message)
async def update_password_me(body: UpdatePassword, current_user: UserInDB = Depends(get_current_user)):
    if not verify_password(body.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    if body.current_password == body.new_password:
        raise HTTPException(status_code=400, detail="New password cannot be the same as the current one")
    hashed_password = get_password_hash(body.new_password)
    await db.users.update_one({"_id": current_user.id}, {"$set": {"hashed_password": hashed_password}})
    return Message(message="Password updated successfully")

@router.get("/me", response_model=UserPublic)
async def read_user_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user

@router.delete("/me", response_model=Message)
async def delete_user_me(current_user: UserInDB = Depends(get_current_user)):
    if current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Super users are not allowed to delete themselves")
    await db.users.delete_one({"_id": current_user.id})
    return Message(message="User deleted successfully")

@router.post("/signup", response_model=UserPublic)
async def register_user(user_in: UserCreate):
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(status_code=403, detail="Open user registration is forbidden on this server")
    user = await get_user_by_email(user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="The user with this email already exists in the system")
    user = await create_user(user_in)
    return user

@router.get("/{user_id}", response_model=UserPublic)
async def read_user_by_id(user_id: str, current_user: UserInDB = Depends(get_current_user)):
    user = await db.users.find_one({"_id": user_id})
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    return user

@router.patch("/{user_id}", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic)
async def update_user(user_id: str, user_in: UserUpdate):
    user = await db.users.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="The user with this id does not exist in the system")
    if user_in.email:
        existing_user = await get_user_by_email(user_in.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(status_code=409, detail="User with this email already exists")
    user = await update_user(user_id, user_in)
    return user

@router.delete("/{user_id}", dependencies=[Depends(get_current_active_superuser)], response_model=Message)
async def delete_user(user_id: str, current_user: UserInDB = Depends(get_current_user)):
    user = await db.users.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user == current_user:
        raise HTTPException(status_code=403, detail="Super users are not allowed to delete themselves")
    await db.users.delete_one({"_id": user_id})
    return Message(message="User deleted successfully")