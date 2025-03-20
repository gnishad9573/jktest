import asyncio
import asyncpg
import os 
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from core.config import Settings
from db.base_class import Baseclass


DATABASE_URL = Settings.postgres_url
DATABASE_URL_DB = Settings.postgres_url_db

engine = create_async_engine(DATABASE_URL, future=True, echo=True)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

async def create_database():
    db_name = "bookstore" 
    temp_conn = await asyncpg.connect(DATABASE_URL_DB)
    
    result = await temp_conn.fetchval("SELECT 1 FROM pg_database WHERE datname=$1", db_name)
    if result:
        print(f"Database '{db_name}' already exists.")
    else:
        await temp_conn.execute(f"CREATE DATABASE {db_name}")
        print(f"Database '{db_name}' created successfully!")

    await temp_conn.close()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Baseclass.metadata.create_all)


   


