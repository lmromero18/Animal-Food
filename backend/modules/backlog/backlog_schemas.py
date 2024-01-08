from datetime import datetime
from typing import List, Optional
from uuid import UUID
from modules.product.product_schemas import ProductInDB

from pydantic import BaseModel

class BacklogBase(BaseModel):
    product_id: Optional[UUID] | None

class BacklogCreate(BacklogBase):
    product_id: UUID
    required_quantity: Optional[int]

class BacklogToSave(BacklogCreate):
    created_by: Optional[UUID]
    updated_by: Optional[UUID]
    
class BacklogUpdate(BacklogBase):
    product_id: Optional[UUID]
    required_quantity: Optional[int]
    is_active: Optional[bool]

class BacklogInDB(BacklogBase):
    id: UUID
    required_quantity: Optional[int]
    product_id: Optional[UUID]
    product: Optional[ProductInDB]
    is_active: Optional[bool]
    created_by: Optional[UUID]
    updated_by: Optional[UUID]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def dict(self, *args, **kwargs):
        ordered_fields = ["id", "required_quantity", "product_id", "product", "created_by", "updated_by", "created_at", "updated_at"]
        new_fields = {field: getattr(self, field) for field in ordered_fields if hasattr(self, field)}
        return {**new_fields, **super().dict(*args, **kwargs)}

    class Config:
        orm_mode = True
