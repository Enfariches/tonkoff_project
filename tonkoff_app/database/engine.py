from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import text, create_engine, select
from database.models import Profile
import asyncio

DB_CONFIG = "postgresql+asyncpg://postgres:root@localhost:5432/bot"
engine = create_async_engine(DB_CONFIG)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

