from fastapi import APIRouter
from sqlalchemy.future import select
from app.core.db import async_session
from app.models.rbac import Role, Permission

router = APIRouter()

@router.get("/permissions")
async def list_permissions():
    async with async_session() as session:
        result = await session.execute(select(Permission))
        permissions = result.scalars().all()
        return [{"code": p.code, "description": p.description} for p in permissions]

@router.get("/roles")
async def list_roles():
    async with async_session() as session:
        result = await session.execute(select(Role))
        roles = result.scalars().all()
        return [{"id": str(r.id), "name": r.name} for r in roles]
