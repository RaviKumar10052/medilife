from typing import List
from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserRead
from app.modules.users.service import create_user, get_all_users

router = APIRouter()

@router.post("/", response_model=UserRead)
async def register_user(user: UserCreate):
    created = await create_user(user.username, user.email, user.password)
    return created

@router.get("/", response_model=List[UserRead])
async def list_users():
    users = await get_all_users()
    return users
