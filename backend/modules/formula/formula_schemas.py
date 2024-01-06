from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from modules.raw_material.raw_material_schemas import RawMaterialInDB
from modules.product.product_schemas import ProductInDB

from pydantic import BaseModel

from modules.warehouse.warehouse_schemas import WarehouseInDB


class FormulaBase(BaseModel):
    required_quantity: Optional[int] | None
    product_id: Optional[UUID] | None
    raw_material_id: Optional[UUID] | None

class FormulaCreate(FormulaBase):
    required_quantity: int 
    product_id: Optional[UUID] 
    raw_material_id: Optional[UUID]

class FormulaToSave(FormulaCreate):
    created_by: Optional[UUID]
    updated_by: Optional[UUID]

class FormulaUpdate(FormulaBase):
    required_quantity: Optional[int]
    product_id: Optional[UUID]
    raw_material_id: Optional[UUID]
    is_active: Optional[bool]

class FormulaInDB(FormulaBase):
    id: UUID
    required_quantity: Optional[int]
    is_active: Optional[bool]
    raw_material_id: Optional[UUID]
    raw_material: Optional[RawMaterialInDB]
    product_id: Optional[UUID]    
    product: Optional[ProductInDB]    
    created_by: Optional[UUID]
    updated_by: Optional[UUID]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def dict(self, *args, **kwargs):
        ordered_fields = [
            "id", "is_active" ,"product_id", "product", "raw_material_id", "raw_material", "required_quantity", 
            "created_by", "updated_by", "created_at", "updated_at",
        ]
        new_fields = {field: getattr(self, field) for field in ordered_fields if hasattr(self, field)}
        return {**new_fields, **super().dict(*args, **kwargs)}

    class Config:
        orm_mode = True