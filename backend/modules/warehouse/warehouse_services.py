from typing import List
from uuid import UUID

from databases import Database
from fastapi import logger
from shared.utils.service_result import ServiceResult
from modules.warehouse.warehouse_repositories import WarehouseRepository
from modules.warehouse.warehouse_exceptions import WarehouseExceptions
from modules.warehouse.warehouse_schemas import (
    WarehouseCreate,
    WarehouseToSave,
)
from modules.users.users.user_schemas import UserInDB

class WarehouseService:
    def __init__(self, db: Database):
        self.db = db

    async def create_warehouse(
    self, warehouse: WarehouseCreate, current_user: UserInDB):

        new_warehouse = WarehouseToSave(**warehouse.dict())
        new_warehouse.created_by = current_user.id
        new_warehouse.updated_by = current_user.id

        warehouse_item = await WarehouseRepository(self.db).create_warehouse(new_warehouse)

        if not warehouse_item:
            logger.error("Error creating warehouse")
            return ServiceResult(WarehouseExceptions.WarehouseCreateException())

        return ServiceResult(warehouse_item)
