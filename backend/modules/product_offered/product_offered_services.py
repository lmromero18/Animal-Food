from typing import List
from uuid import UUID
import uuid
from modules.warehouse.warehouse_exceptions import WarehouseExceptions
from modules.warehouse.warehouse_services import WarehouseService
from shared.utils.record_to_dict import record_to_dict
from shared.utils.verify_uuid import is_valid_uuid

from databases import Database
import fastapi
from loguru import logger

from shared.utils.service_result import ServiceResult
from modules.product_offered.product_offered_repositories import ProductOfferedRepository
from modules.product_offered.product_offered_exceptions import ProductOfferedExceptions
from modules.product_offered.product_offered_schemas import (
    ProductOfferedCreate,
    ProductOfferedToSave,
    ProductOfferedInDB,
    ProductOfferedUpdate
)
from modules.users.users.user_schemas import UserInDB
from shared.core.config import API_PREFIX
import shared.utils.repository_utils as ru
from shared.utils.short_pagination import short_pagination

class ProductOfferedService:
    def __init__(self, db: Database):
        self.db = db
  
    async def create_product_offered(
        self, product_offered: ProductOfferedCreate, current_user: UserInDB):

        new_product_offered = ProductOfferedToSave(**product_offered.dict())
        new_product_offered.created_by = current_user.id
        new_product_offered.updated_by = uuid.UUID(int=0)

        product_offered_item = await ProductOfferedRepository(self.db).create_product_offered(new_product_offered)

        if product_offered_item == 'false':
            logger.error("Formula requirements not met for product offered")
            return ServiceResult(ProductOfferedExceptions.ProductOfferedRequirementsNotMetCreateException())
        elif not product_offered_item:
            logger.error("Error creating product offered")
            return ServiceResult(ProductOfferedExceptions.ProductOfferedCreateException())


        return ServiceResult(product_offered_item)
    
    async def get_product_offered_list(
        self,
        search: str | None,
        page_num: int = 1,
        page_size: int = 10,
        order: str = None,
        direction: str = None,
    ) -> ServiceResult:
        product_offered_list = await ProductOfferedRepository(self.db).get_product_offered_list(search, order, direction)

        service_result = None
        if len(product_offered_list) == 0:
            service_result = ServiceResult([])
            service_result.status_code = 204
        else:
            response = short_pagination(
                page_num=page_num,
                page_size=page_size,
                data_list=product_offered_list,
                route=f"{API_PREFIX}/product-offered",
            )
            service_result = ServiceResult(response)

        return service_result
    
    async def get_product_offered_by_id(self, id: UUID) -> ServiceResult:
        product_offered_in_db = await ProductOfferedRepository(self.db).get_product_offered_by_id(id=id)

        if isinstance(product_offered_in_db, dict) and not product_offered_in_db.get("id"):
            logger.info("The requested product offered is not in the database")
            return ServiceResult(ProductOfferedExceptions.ProductOfferedNotFoundException())

        product_offered = ProductOfferedInDB(**product_offered_in_db.dict())
        return ServiceResult(product_offered)
    
    async def update_product_offered(
        self, id: UUID, product_offered_update: ProductOfferedUpdate, current_user: UserInDB
    ) -> ServiceResult:
        if not is_valid_uuid(id):
            return ServiceResult(ProductOfferedExceptions.ProductOfferedIdNoValidException())

        try:
            product_offered = await ProductOfferedRepository(self.db).update_product_offered(
                id=id,
                product_offered_update=product_offered_update,
                updated_by_id=current_user.id,
            )
            
            logger.info(f"product_offered: {product_offered}")

            if isinstance(product_offered, dict) and not product_offered.get("id"):
                logger.info("The ID of the product offered to update is not in the database")
                return ServiceResult(ProductOfferedExceptions.ProductOfferedNotFoundException())

            return ServiceResult(ProductOfferedInDB(**product_offered.dict()))

        except Exception as e:
            logger.error(f"Error: {e}")
            return ServiceResult(ProductOfferedExceptions.ProductOfferedInvalidUpdateParamsException(e))
    
    async def delete_product_offered_by_id(
        self, id: UUID
    ) -> ServiceResult:
        
        product_offered_id = await ProductOfferedRepository(self.db).delete_product_offered_by_id(id=id)

        if isinstance(product_offered_id, dict) and not product_offered_id.get("id"):
            logger.info("The ID of the product offered to delete is not in the database")
            return ServiceResult(ProductOfferedExceptions.ProductOfferedNotFoundException())
        
        return ServiceResult(product_offered_id)