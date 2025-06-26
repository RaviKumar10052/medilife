from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Async engine for SQLite (or any DB defined in .env)
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

# Create async session factory
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base model class
Base = declarative_base()

# Dependency to get DB session
async def get_db():
    async with async_session() as session:
        yield session

# Called at startup to create all tables
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
