from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# DATABASE_URL = f"postgresql+asyncpg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in environment")

# async engine
engine = create_async_engine(DATABASE_URL, echo=False, future=True)

# async session factory
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session