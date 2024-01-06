from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from modules.raw_material.raw_material_schemas import RawMaterialInDB
from modules.supplier.supplier_schemas import SupplierInDB
from modules.price.price_schemas import PriceInDB

from pydantic import BaseModel

class PurchaseBase(BaseModel):
    supplier_id: Optional[UUID] | None
    raw_material_id: Optional[UUID] | None
    quantity: Optional[int] | None

class PurchaseCreate(PurchaseBase):
    supplier_id: UUID
    raw_material_id: UUID
    quantity: int

class PurchaseToSave(PurchaseCreate):
    is_delivered: Optional[bool]
    order_date: Optional[datetime]
    created_by: Optional[UUID]
    updated_by: Optional[UUID]

class PurchaseUpdate(PurchaseBase):
    supplier_id: Optional[UUID]
    raw_material_id: Optional[UUID]
    delivery_date: Optional[datetime]
    quantity: Optional[int]
    is_delivered: Optional[bool]


class PurchaseInDB(PurchaseBase):
    id: UUID
    supplier_id: Optional[UUID]
    supplier: Optional[SupplierInDB]
    order_date: Optional[datetime]
    delivery_date: Optional[datetime]
    raw_material_id: Optional[UUID]
    raw_material: Optional[RawMaterialInDB]
    quantity: Optional[int]
    is_delivered: Optional[bool]
    is_active: Optional[bool]  
    created_by: Optional[UUID]
    updated_by: Optional[UUID]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def dict(self, *args, **kwargs):
        ordered_fields = ["id", "supplier_id", "supplier" "order_date", "delivery_date", "raw_material_id", "raw_material", "quantity", "is_active","is_delivered", "created_by", "updated_by", "created_at", "updated_at"]
        new_fields = {field: getattr(self, field) for field in ordered_fields if hasattr(self, field)}
        return {**new_fields, **super().dict(*args, **kwargs)}

    class Config:
        orm_mode = True
