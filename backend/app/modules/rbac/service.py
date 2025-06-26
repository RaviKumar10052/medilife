from sqlalchemy.future import select
from app.models.rbac import API, Permission, APIToPermission
from app.core.db import async_session

async def get_api_permission(method: str, path: str) -> Permission:
    async with async_session() as session:
        result = await session.execute(
            select(Permission).join(APIToPermission).join(API).where(
                API.method == method,
                API.path == path
            )
        )
        return result.scalars().first()

async def user_has_permission(user, permission_code: str) -> bool:
    return any(
        permission.code == permission_code
        for role in user.roles
        for permission in role.permissions
    )
