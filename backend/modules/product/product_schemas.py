from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

class ProductBase(BaseModel):
    name: Optional[str] | None
    description: Optional[str] | None

class ProductCreate(ProductBase):
    name: str
    description: str

class ProductToSave(ProductCreate):
    created_by: Optional[UUID]
    updated_by: Optional[UUID]

class ProductUpdate(ProductBase):
    name: Optional[str]
    description: Optional[str]
    price_id: Optional[UUID]
    is_active: Optional[bool]

class ProductInDB(ProductBase):
    id: UUID
    name: Optional[str]
    description: Optional[str]
    is_active: Optional[bool]
    created_by: Optional[UUID]
    updated_by: Optional[UUID]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def dict(self, *args, **kwargs):
        ordered_fields = ["id", "name", "is_active" ,"description", "created_by", "updated_by", "created_at", "updated_at", ]
        new_fields = {field: getattr(self, field) for field in ordered_fields if hasattr(self, field)}
        return {**new_fields, **super().dict(*args, **kwargs)}

    class Config:
        orm_mode = True