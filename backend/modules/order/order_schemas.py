from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from modules.product_offered.product_offered_schemas import ProductOfferedInDB
from pydantic import BaseModel

class OrderBase(BaseModel):
    product_offered_id: Optional[UUID] | None
    quantity: Optional[Decimal] | None
    discount: Optional[Decimal] | None

class OrderCreate(OrderBase):
    product_offered_id: UUID
    quantity: Decimal
    discount: Decimal

class OrderToSave(OrderCreate):
    is_delivered: Optional[bool]
    total: Optional[Decimal]
    order_date: Optional[datetime]
    created_by: Optional[UUID]
    updated_by: Optional[UUID]

class OrderUpdate(OrderBase):
    product_offered_id: Optional[UUID]
    quantity: Optional[Decimal]
    discount: Optional[Decimal]
    is_delivered: Optional[bool]

class OrderInDB(OrderBase):
    id: UUID
    product_offered_id: Optional[UUID]
    product_offered: Optional[ProductOfferedInDB]
    quantity: Optional[Decimal]
    order_date: Optional[datetime]
    delivery_date: Optional[datetime]
    discount: Optional[Decimal]
    total: Optional[Decimal]
    is_delivered: Optional[bool]
    is_active: Optional[bool]  
    created_by: Optional[UUID]
    updated_by: Optional[UUID]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def dict(self, *args, **kwargs):
        ordered_fields = ["id", "product_offered_id", "quantity", "order_date", "delivery_date", "discount", "total", "is_active","is_delivered", "created_by", "updated_by", "created_at", "updated_at"]
        new_fields = {field: getattr(self, field) for field in ordered_fields if hasattr(self, field)}
        return {**new_fields, **super().dict(*args, **kwargs)}

    class Config:
        orm_mode = True
