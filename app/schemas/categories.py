from pydantic import BaseModel, Field, ConfigDict


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)

class Category(BaseModel):
    id: int = Field(...)
    name: str = Field(...)

    model_config = ConfigDict(from_attributes=True)

