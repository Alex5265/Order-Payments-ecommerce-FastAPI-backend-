from sqlalchemy import Column, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.database import Base

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    parent: Mapped["Category | None"] = relationship("Category",
                                                     back_populates="children",
                                                     remote_side="Category.id")
    children: Mapped[list["Category"]] = relationship("Category",
                                                      back_populates='parent')