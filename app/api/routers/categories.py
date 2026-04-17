from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.core.dependencies import get_category_service
from app.schemas.categories import Category, CategoryBase
from app.services.categories import CategoryService


router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)

@router.get("/", response_model=List[Category])
async def read_all_categories(
        skip: int = 0,
        limit: int = 100,
        category_service: CategoryService = Depends(get_category_service)
):
    """
    Returns a list of all product categories
    """
    return await category_service.get_all_categories(skip=skip, limit=limit)

@router.get("/{category_id}", response_model=Category)
async def read_category(
        category_id: int,
        category_service: CategoryService = Depends(get_category_service)

):
    """
    Returns category by its ID
    """
    return await category_service.get_category_by_id(category_id=category_id)

@router.put("/{category_id}")
async def update_category(
        category_id: int,
        category: CategoryBase,
        category_service: CategoryService = Depends(get_category_service)
):
    """
    Updates a category by its ID
    """
    return await category_service.update_category(category_id, category)

@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(
        category: CategoryBase,
        category_service: CategoryService = Depends(get_category_service)
):
    """
    Creates a new category
    """
    return await category_service.create_category(category=category)

@router.delete("/{category_id}")
async def delete_category(
        category_id: int,
        category_service: CategoryService = Depends(get_category_service)
):
    """
    Deletes a category by its ID
    """
    return await category_service.delete_category(category_id=category_id)

