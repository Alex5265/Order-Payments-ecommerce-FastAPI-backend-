from pydantic import BaseModel, Field, ConfigDict


class CategoryBase(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=50, description="Category name (3-50 characters)")
    parent_id: int | None = Field(default=None, description="Parent category ID, if any")

class Category(BaseModel):
    id: int = Field(..., description="Unique category identifier")
    name: str = Field(..., description="Category name (3-50 characters)")
    parent_id: int | None = Field(default=None, description="Parent category ID, if any")
    is_active: bool = Field(..., description="Category activity")

    model_config = ConfigDict(from_attributes=True)

