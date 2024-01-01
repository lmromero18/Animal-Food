from typing import List, Optional
from uuid import UUID

from shared.utils.schemas_base import BaseSchema, DateTimeModelMixin, IDModelMixin

class WarehouseBase(BaseSchema):
    type: str | None 
    number: int | None
    name: Optional[str]

class WarehouseCreate(WarehouseBase):
    type: str
    number: Optional[int] = None
    name: Optional[str] = None

class WarehouseToSave(WarehouseCreate):
    created_by: UUID | None
    updated_by: UUID | None

class WarehouseInDB(WarehouseBase,IDModelMixin, DateTimeModelMixin):
    created_by: UUID | None
    updated_by: UUID | None
    number: int | None