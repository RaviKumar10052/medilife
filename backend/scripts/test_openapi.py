from fastapi.openapi.utils import get_openapi
from app.main import app

schema = get_openapi(
    title=app.title,
    version=app.version,
    routes=app.routes
)

print("OpenAPI schema generated successfully")
