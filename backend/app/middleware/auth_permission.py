from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from app.core.auth import decode_token
from app.modules.users.service import get_user_by_id
from app.modules.rbac.service import get_api_permission, user_has_permission

EXCLUDE_PATHS = {"/docs", "/openapi.json", "/favicon.ico", "/redoc"}

class AuthPermissionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in EXCLUDE_PATHS:
            return await call_next(request)
         
        token = request.headers.get("Authorization")
        if token and token.startswith("Bearer "):
            token = token[7:]
            payload = decode_token(token)
            if not payload or "sub" not in payload:
                raise HTTPException(status_code=401, detail="Invalid token")

            user_id = payload["sub"]
            user = await get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=401, detail="User not found")

            request.state.user = user
        else:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        # Permission check (based on method + path)
        method = request.method
        path = request.url.path

        permission = await get_api_permission(method, path)
        if permission and not await user_has_permission(user, permission.code):
            raise HTTPException(status_code=403, detail="Permission denied")

        return await call_next(request)
