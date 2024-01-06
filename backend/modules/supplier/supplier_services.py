from typing import List
from uuid import UUID
import uuid
from shared.utils.verify_uuid import is_valid_uuid

from databases import Database
import fastapi
from loguru import logger

from shared.utils.service_result import ServiceResult
from modules.supplier.supplier_repositories import SupplierRepository
from modules.supplier.supplier_exceptions import SupplierExceptions
from modules.supplier.supplier_schemas import (
    SupplierCreate,
    SupplierToSave,
    SupplierInDB,
    SupplierUpdate
)
from modules.users.users.user_schemas import UserInDB
from shared.core.config import API_PREFIX
import shared.utils.repository_utils as ru
from shared.utils.short_pagination import short_pagination

class SupplierService:
    def __init__(self, db: Database):
        self.db = db

    async def create_supplier(
        self, supplier: SupplierCreate, current_user: UserInDB):

        new_supplier = SupplierToSave(**supplier.dict())
        new_supplier.created_by = current_user.id
        new_supplier.updated_by = uuid.UUID(int=0)

        supplier_item = await SupplierRepository(self.db).create_supplier(new_supplier)

        if not supplier_item:
            logger.error("Error creating supplier")
            return ServiceResult(SupplierExceptions.SupplierCreateException())

        return ServiceResult(supplier_item)
    
    async def get_supplier_list(
        self,
        search: str | None,
        page_num: int = 1,
        page_size: int = 10,
        order: str = None,
        direction: str = None,
    ) -> ServiceResult:
        suppliers = await SupplierRepository(self.db).get_supplier_list(search, order, direction)

        service_result = None
        if len(suppliers) == 0:
            service_result = ServiceResult([])
            service_result.status_code = 204
        else:
            response = short_pagination(
                page_num=page_num,
                page_size=page_size,
                data_list=suppliers,
                route=f"{API_PREFIX}/suppliers",
            )
            service_result = ServiceResult(response)

        return service_result
    
    async def get_supplier_by_id(self, id: UUID) -> ServiceResult:
        supplier_in_db = await SupplierRepository(self.db).get_supplier_by_id(id=id)

        if isinstance(supplier_in_db, dict) and not supplier_in_db.get("id"):
            logger.info("The requested supplier is not in the database")
            return ServiceResult(SupplierExceptions.SupplierNotFoundException())

        supplier = SupplierInDB(**supplier_in_db.dict())
        return ServiceResult(supplier)
    
    async def update_supplier(
        self, id: UUID, supplier_update: SupplierUpdate, current_user: UserInDB
    ) -> ServiceResult:
        if not is_valid_uuid(id):
            return ServiceResult(SupplierExceptions.SupplierIdNoValidException())

        try:
            supplier = await SupplierRepository(self.db).update_supplier(
                id=id,
                supplier_update=supplier_update,
                updated_by_id=current_user.id,
            )

            if isinstance(supplier, dict) and not supplier.get("id"):
                logger.info("The supplier ID to update is not in the database")
                return ServiceResult(SupplierExceptions.SupplierNotFoundException())

            return ServiceResult(SupplierInDB(**supplier.dict()))

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return ServiceResult(SupplierExceptions.SupplierInvalidUpdateParamsException(e))
    
    async def delete_supplier_by_id(
        self, id: UUID
    ) -> ServiceResult:
        
        supplier_id = await SupplierRepository(self.db).delete_supplier_by_id(id=id)

        if isinstance(supplier_id, dict) and not supplier_id.get("id"):
            logger.info("The supplier ID to delete is not in the database")
            return ServiceResult(SupplierExceptions.SupplierNotFoundException())
        
        return ServiceResult(supplier_id)
