import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.db import create_db_and_tables
from app.modules import register_all_routers
from app.middleware.auth_permission import AuthPermissionMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    register_all_routers(app)
    await create_db_and_tables()
    yield
    # Shutdown logic (optional cleanup)

app = FastAPI(title="Medilife API", lifespan=lifespan)

# Add auth + permission middleware
app.add_middleware(AuthPermissionMiddleware)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
