from fastapi import FastAPI
from app.modules.auth.api import router as auth_router
from app.modules.users.api import router as users_router
from app.modules.rbac.api import router as rbac_router

def register_all_routers(app: FastAPI):
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
    app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])
    app.include_router(rbac_router, prefix="/api/v1/rbac", tags=["RBAC"])
