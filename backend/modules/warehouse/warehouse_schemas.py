from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

class WarehouseBase(BaseModel):
    type: Optional[str]

class WarehouseCreate(WarehouseBase):
    type: str

class WarehouseToSave(WarehouseCreate):
    created_by: Optional[UUID]
    updated_by: Optional[UUID]
    
class WarehouseUpdate(WarehouseBase):
    type: Optional[str]
    is_active: Optional[bool]

class WarehouseInDB(WarehouseBase):
    id: UUID
    name: Optional[str]
    is_active: Optional[bool]
    created_by: Optional[UUID]
    updated_by: Optional[UUID]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def dict(self, *args, **kwargs):
        ordered_fields = ["id", "type","name", "created_by", "updated_by", "created_at", "updated_at"]
        new_fields = {field: getattr(self, field) for field in ordered_fields if hasattr(self, field)}
        return {**new_fields, **super().dict(*args, **kwargs)}

    class Config:
        orm_mode = True