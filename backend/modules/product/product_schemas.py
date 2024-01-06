from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from modules.price.price_schemas import PriceInDB

from pydantic import BaseModel

class ProductBase(BaseModel):
    name: Optional[str] | None
    description: Optional[str] | None
    price_id: Optional[UUID] | None

class ProductCreate(ProductBase):
    name: str
    description: str
    price_id: UUID

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
    price_id: Optional[UUID]
    price: Optional[PriceInDB]
    created_by: Optional[UUID]
    updated_by: Optional[UUID]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def dict(self, *args, **kwargs):
        ordered_fields = ["id", "name", "description", "price_id", "price", "created_by", "updated_by", "created_at", "updated_at", ]
        new_fields = {field: getattr(self, field) for field in ordered_fields if hasattr(self, field)}
        return {**new_fields, **super().dict(*args, **kwargs)}

    class Config:
        orm_mode = True