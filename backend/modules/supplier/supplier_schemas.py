from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class SupplierBase(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None

class SupplierCreate(SupplierBase):
    name: str
    address: str

class SupplierToSave(SupplierCreate):
    created_by: Optional[UUID]
    updated_by: Optional[UUID]

class SupplierUpdate(SupplierBase):
    name: Optional[str]
    address: Optional[str]
    is_active: Optional[bool]

class SupplierInDB(SupplierBase):
    id: UUID
    name: Optional[str]
    address: Optional[str]
    is_active: Optional[bool]
    created_by: Optional[UUID]
    updated_by: Optional[UUID]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def dict(self, *args, **kwargs):
        ordered_fields = ["id", "name", "address", "created_by", "updated_by", "created_at", "updated_at"]
        new_fields = {field: getattr(self, field) for field in ordered_fields if hasattr(self, field)}
        return {**new_fields, **super().dict(*args, **kwargs)}

    class Config:
        orm_mode = True
