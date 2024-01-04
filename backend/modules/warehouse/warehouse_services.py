from typing import List
from uuid import UUID
import uuid
from shared.utils.record_to_dict import record_to_dict
from shared.utils.verify_uuid import is_valid_uuid


from databases import Database
import fastapi
from loguru import logger

from shared.utils.service_result import ServiceResult
from modules.warehouse.warehouse_repositories import WarehouseRepository
from modules.warehouse.warehouse_exceptions import WarehouseExceptions
from modules.warehouse.warehouse_schemas import (
    WarehouseCreate,
    WarehouseToSave,
    WarehouseInDB,
    WarehouseUpdate
)
from modules.users.users.user_schemas import UserInDB
from shared.core.config import API_PREFIX
import shared.utils.repository_utils as ru
from shared.utils.short_pagination import short_pagination

class WarehouseService:
    def __init__(self, db: Database):
        self.db = db

    async def create_warehouse(
    self, warehouse: WarehouseCreate, current_user: UserInDB):

        new_warehouse = WarehouseToSave(**warehouse.dict())
        new_warehouse.created_by = current_user.id
        new_warehouse.updated_by = uuid.UUID(int=0)

        warehouse_item = await WarehouseRepository(self.db).create_warehouse(new_warehouse)

        if not warehouse_item:
            logger.error("Error creating warehouse")
            return ServiceResult(WarehouseExceptions.WarehouseCreateException())

        return ServiceResult(warehouse_item)
    
    async def get_warehouse_list(
        self,
        search: str | None,
        page_num: int = 1,
        page_size: int = 10,
        order: str = None,
        direction: str = None,
    ) -> ServiceResult:
        warehouse = await WarehouseRepository(self.db).get_warehouse_list(search, order, direction)

        service_result = None
        if len(warehouse) == 0:
            service_result = ServiceResult([])
            service_result.status_code = 204
        else:
            response = short_pagination(
                page_num=page_num,
                page_size=page_size,
                data_list=warehouse,
                route=f"{API_PREFIX}/warehouse",
            )
            service_result = ServiceResult(response)

        return service_result
    
    async def get_warehouse_by_id(self, id: UUID) -> ServiceResult:
        warehouse_in_db = await WarehouseRepository(self.db).get_warehouse_by_id(id=id)

        if isinstance(warehouse_in_db, dict) and not warehouse_in_db.get("id"):
            logger.info("El almacén solicitado no está en base de datos")
            return ServiceResult(WarehouseExceptions.WarehouseNotFoundException())

        warehouse = WarehouseInDB(**warehouse_in_db.dict())
        return ServiceResult(warehouse)
    
    async def update_warehouse(
        self, id: UUID, warehouse_update: WarehouseUpdate, current_user: UserInDB
    ) -> ServiceResult:
        if not is_valid_uuid(id):
            return ServiceResult(WarehouseExceptions.WarehouseIdNoValidException())

        try:
            warehouse = await WarehouseRepository(self.db).update_warehouse(
                id=id,
                warehouse_update=warehouse_update,
                updated_by_id=current_user.id,
            )

            if isinstance(warehouse, dict) and not warehouse.get("id"):
                logger.info("El ID del almacén a actualizar no está en base de datos")
                return ServiceResult(WarehouseExceptions.WarehouseNotFoundException())

            return ServiceResult(WarehouseInDB(**warehouse.dict()))

        except Exception as e:
            logger.error(f"Se produjo un error: {e}")
            return ServiceResult(WarehouseExceptions.WarehouseInvalidUpdateParamsException(e))
    
    async def delete_warehouse_by_id(
        self, id: UUID
    ) -> ServiceResult:
        
        warehouse_id = await WarehouseRepository(self.db).delete_warehouse_by_id(id=id)

        if isinstance(warehouse_id, dict) and not warehouse_id.get("id"):
                logger.info("El ID de tarea a eliminar no está en base de datos")
                return ServiceResult(WarehouseExceptions.WarehouseNotFoundException())
        
        return  ServiceResult(warehouse_id)
