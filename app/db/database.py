import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base

DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/database"

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    for attempt in range(10):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            print("Database is ready!")
            return
        except Exception as e:
            print(f"Database not ready yet, retrying... ({attempt + 1}/10)")
            await asyncio.sleep(2)

    raise Exception("Failed to connect to the database after 10 attempts")

async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
