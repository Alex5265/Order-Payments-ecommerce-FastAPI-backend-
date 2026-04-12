from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.core.database import async_session_maker
from app.repositories.categories import CategoryRepository
from app.services.categories import CategoryService


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


# Dependencies for obtaining repository instances
def get_category_repository(db: AsyncSession = Depends(get_async_db)) -> CategoryRepository:
    return CategoryRepository(db=db)



# Dependencies for obtaining service instances
def get_category_service(repo: CategoryRepository = Depends(get_category_repository)) -> CategoryService:
    return CategoryService(category_repo=repo)