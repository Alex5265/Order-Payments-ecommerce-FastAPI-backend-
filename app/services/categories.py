from collections.abc import Sequence
from fastapi import HTTPException, status

from app.repositories.categories import CategoryRepository
from app.schemas.categories import CategoryBase
from app.models.categories import Category


class CategoryService:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    async def get_all_categories(self, skip: int = 0, limit: int = 100) -> Sequence[Category]:
        db_categories = await self.category_repo.get_all(skip=skip, limit=limit)
        return db_categories

    async def get_category_by_id(self, category_id: int) -> Category | None:
        db_category = await self.category_repo.get_by_id(category_id=category_id)
        if db_category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return db_category

    async def create_category(self, category: CategoryBase) -> Category | None:
        # name check
        if category.name is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="category must be name")

        # checking parent availability
        if category.parent_id is not None:
            existing_parent = await self.category_repo.get_by_id(category_id=category.parent_id)
            if existing_parent is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Parent category not found")

        # checking category availability
        existing_category = await self.category_repo.get_by_name(category.name)
        if existing_category:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category with this name already exists")

        return await self.category_repo.create(category)

    async def update_category(self, category_id, category: CategoryBase) -> Category | None:
        # checking parent availability
        if category.parent_id is not None:
            existing_parent = await self.category_repo.get_by_id(category_id=category.parent_id)
            if existing_parent is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Parent category not found")

        existing_category = await self.get_category_by_id(category_id)
        return await self.category_repo.update(category_id, category)

    async def delete_category(self,  category_id: int) -> Category | None:
        existing_category = await self.get_category_byid(category_id)
        return await self.category_repo.delete(category_id)