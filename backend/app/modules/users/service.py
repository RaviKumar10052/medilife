from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from passlib.context import CryptContext
from app.core.db import async_session
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def create_user(username: str, email: str, password: str):
    async with async_session() as session:
        user = User(
            username=username,
            email=email,
            hashed_password=get_password_hash(password)
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

async def authenticate_user(username: str, password: str):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalars().first()
        if user and verify_password(password, user.hashed_password):
            return user
        return None

async def get_user_by_id(user_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

async def get_all_users():
    async with async_session() as session:
        result = await session.execute(select(User))
        return result.scalars().all()
