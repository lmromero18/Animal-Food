from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from modules.product.product_schemas import ProductInDB

from pydantic import BaseModel

from modules.warehouse.warehouse_schemas import WarehouseInDB


class ProductOfferedBase(BaseModel):
    name: Optional[str] | None
    quantity: Optional[int] | None
    price: Optional[Decimal] | None
    product_id: Optional[UUID] | None
    warehouse_id: Optional[UUID] | None


class ProductOfferedCreate(ProductOfferedBase):
    name: str
    quantity: Optional[int]
    price: Optional[Decimal]


class ProductOfferedToSave(ProductOfferedCreate):
    code: Optional[str]
    created_by: Optional[UUID]
    updated_by: Optional[UUID]


class ProductOfferedUpdate(ProductOfferedBase):
    name: Optional[str]
    quantity: Optional[int]
    price: Optional[Decimal]
    product_id: Optional[UUID]
    warehouse_id: Optional[UUID]
    is_active: Optional[bool]


class ProductOfferedInDB(ProductOfferedBase):
    id: UUID
    name: Optional[str]
    code: Optional[str]
    quantity: Optional[int]
    price: Optional[Decimal]
    warehouse_id: Optional[UUID]
    warehouse: Optional[WarehouseInDB]
    product_id: Optional[UUID]
    product: Optional[ProductInDB]
    created_by: Optional[UUID]
    updated_by: Optional[UUID]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def dict(self, *args, **kwargs):
        ordered_fields = [
            "id", "name", "code", "quantity", "price", "product_id", "product", 
            "warehouse_id", "warehouse","created_by", "updated_by", "created_at", "updated_at",
        ]
        new_fields = {field: getattr(self, field) for field in ordered_fields if hasattr(self, field)}
        return {**new_fields, **super().dict(*args, **kwargs)}

    class Config:
        orm_mode = True