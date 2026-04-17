from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.models.categories import Category
from app.schemas.categories import Category as CategorySchema, CategoryBase

class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, category_id: int) -> Category | None:
        result = await self.db.scalars(
            select(Category).filter(Category.id == category_id,
                                    Category.is_active == True)
        )
        return result.first()

    async def get_by_name(self, name: str) -> Category | None:
        result = await self.db.scalars(
            select(Category).filter(Category.name == name,
                                    Category.is_active == True)
        )
        return result.first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[Category]:
        result = await self.db.scalars(
            select(Category).filter(Category.is_active == True).offset(skip).limit(limit)
        )
        return result.all()

    async def create(self, category: CategoryBase) -> Category:
        db_category = Category(**category.model_dump())
        self.db.add(db_category)
        await self.db.commit()
        await self.db.refresh(db_category)
        return db_category

    async def update(self, category_id: int, category: CategoryBase) -> Category | None:
        db_category = await self.get_by_id(category_id)
        if not db_category:
            return None

        update_data = category.model_dump(exclude_unset=True)
        await self.db.execute(
            update(Category).where(Category.id == category_id).values(**update_data)
        )
        await self.db.commit()
        return db_category

    async def delete(self, category_id: int) -> Category | None:
        db_category = await self.get_by_id(category_id)
        await self.db.execute(
            update(Category).where(Category.id == category_id).values(is_active=False)
        )
        await self.db.commit()
        return db_category
