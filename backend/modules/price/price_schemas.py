from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from modules.warehouse.warehouse_schemas import WarehouseInDB

from pydantic import BaseModel


class PriceBase(BaseModel):
    price: Optional[Decimal] | None

class PriceCreate(PriceBase):
    price: Decimal

class PriceToSave(PriceCreate):
    created_by: Optional[UUID]
    updated_by: Optional[UUID]

class PriceUpdate(PriceBase):
    price: Optional[Decimal]   
    is_active: Optional[bool]

class PriceInDB(PriceBase):
    id: UUID
    price: Optional[Decimal]
    is_active: Optional[bool]
    created_by: Optional[UUID]
    updated_by: Optional[UUID]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def dict(self, *args, **kwargs):
        ordered_fields = ["id", "price", "created_by", "updated_by", "created_at", "updated_at"]
        new_fields = {field: getattr(self, field) for field in ordered_fields if hasattr(self, field)}
        return {**new_fields, **super().dict(*args, **kwargs)}

    class Config:
        orm_mode = True
