from databases import Database
from loguru import logger
from typing import List
from uuid import UUID

# from modules.tasks.task_exceptions import TaskExceptions
from modules.warehouse.warehouse_schemas import (
    WarehouseCreate,
    WarehouseInDB,
    WarehouseToSave,
)

from shared.utils.record_to_dict import record_to_dict
import shared.utils.repository_utils as ru

class WarehouseRepository:
    def __init__(self, db: Database):
        self.db = db

    async def create_warehouse(self, warehouse: WarehouseToSave) -> WarehouseInDB:
        from modules.warehouse.warehouse_sqlstatements import CREATE_WAREHOUSE_ITEM

        values = ru.preprocess_create(warehouse.dict())
        record = await self.db.fetch_one(query=CREATE_WAREHOUSE_ITEM, values=values)

        result = record_to_dict(record)

        return WarehouseInDB(**result)
