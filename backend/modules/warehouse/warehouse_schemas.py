from typing import List
from uuid import UUID

from shared.utils.schemas_base import BaseSchema, DateTimeModelMixin, IDModelMixin

class WarehouseBaseSchema(BaseSchema):
    type: str | None 
    number: int | None
    name: str | None

class WarehouseCreateSchema(WarehouseBaseSchema):
    type: str
    number: int
    name: str

class WarehouseToSaveSchema(WarehouseCreateSchema, IDModelMixin, DateTimeModelMixin):
    created_by: UUID | None
    updated_by: UUID | None