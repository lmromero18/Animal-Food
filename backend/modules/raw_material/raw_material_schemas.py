from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from modules.warehouse.warehouse_schemas import WarehouseInDB

from pydantic import BaseModel


class RawMaterialBase(BaseModel):
    name: Optional[str]
    code: Optional[str]
    available_quantity: Optional[int]

class RawMaterialCreate(RawMaterialBase):
    name: str
    code: str
    available_quantity: int

class RawMaterialToSave(RawMaterialCreate):
    created_by: Optional[UUID]
    updated_by: Optional[UUID]

class RawMaterialUpdate(RawMaterialBase):
    name: Optional[str]
    warehouse_id: Optional[UUID]    
    is_active: Optional[bool]

class RawMaterialInDB(RawMaterialBase):
    id: UUID
    name: Optional[str]
    code: Optional[str]
    available_quantity: Optional[int]
    warehouse_id: Optional[UUID]
    warehouse: Optional[WarehouseInDB]   
    created_by: Optional[UUID]
    updated_by: Optional[UUID]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def dict(self, *args, **kwargs):
        ordered_fields = ["id", "name", "code", "available_quantity","warehouse_id","warehouse", "created_by", "updated_by", "created_at", "updated_at"]
        new_fields = {field: getattr(self, field) for field in ordered_fields if hasattr(self, field)}
        return {**new_fields, **super().dict(*args, **kwargs)}

    class Config:
        orm_mode = True