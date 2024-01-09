from typing import List
from uuid import UUID
import uuid
from modules.product.product_exceptions import ProductExceptions
from modules.product.product_repositories import ProductRepository
from shared.utils.verify_uuid import is_valid_uuid

from databases import Database
import fastapi
from loguru import logger

from shared.utils.service_result import ServiceResult
from modules.price.price_repositories import PriceRepository
from modules.price.price_exceptions import PriceExceptions
from modules.price.price_schemas import (
    PriceCreate,
    PriceToSave,
    PriceInDB,
    PriceUpdate
)
from modules.users.users.user_schemas import UserInDB
from shared.core.config import API_PREFIX
import shared.utils.repository_utils as ru
from shared.utils.short_pagination import short_pagination

class PriceService:
    def __init__(self, db: Database):
        self.db = db

    async def create_price(
        self, price: PriceCreate, current_user: UserInDB):

        new_price = PriceToSave(**price.dict())
        new_price.created_by = current_user.id
        new_price.updated_by = uuid.UUID(int=0)        
               
        product_id_exists = await ProductRepository(self.db).get_product_by_id(id=new_price.product_id)
        
        if not product_id_exists:
            logger.info("El producto no existe en base de datos")
            return ServiceResult(ProductExceptions.ProductNotFoundException())
        
        product_id_exists_in_price = await PriceRepository(self.db).get_price_by_product_id(product_id=new_price.product_id)
        
        if product_id_exists_in_price:
            logger.info("El producto ya tiene un precio asignado")
            return ServiceResult(PriceExceptions.PriceProductExistsException())
        
        if new_price.price <= 0:
            logger.info("El precio debe ser mayor a 0")
            return ServiceResult(PriceExceptions.LowPriceException())

        price_item = await PriceRepository(self.db).create_price(new_price)

        if not price_item:
            logger.error("Error creating price")
            return ServiceResult(PriceExceptions.PriceCreateException())

        return ServiceResult(price_item)
    
    async def get_price_list(
        self,
        search: str | None,
        page_num: int = 1,
        page_size: int = 10,
        order: str = None,
        direction: str = None,
    ) -> ServiceResult:
        prices = await PriceRepository(self.db).get_price_list(search, order, direction)

        service_result = None
        if len(prices) == 0:
            service_result = ServiceResult([])
            service_result.status_code = 204
        else:
            response = short_pagination(
                page_num=page_num,
                page_size=page_size,
                data_list=prices,
                route=f"{API_PREFIX}/prices",
            )
            service_result = ServiceResult(response)

        return service_result
    
    async def get_price_by_id(self, id: UUID) -> ServiceResult:
        price_in_db = await PriceRepository(self.db).get_price_by_id(id=id)

        if isinstance(price_in_db, dict) and not price_in_db.get("id"):
            logger.info("The requested price is not in the database")
            return ServiceResult(PriceExceptions.PriceNotFoundException())

        price = PriceInDB(**price_in_db.dict())
        return ServiceResult(price)
    
    async def update_price(
        self, id: UUID, price_update: PriceUpdate, current_user: UserInDB
    ) -> ServiceResult:
        if not is_valid_uuid(id):
            return ServiceResult(PriceExceptions.PriceIdNoValidException())
        
        product_id_exists = await ProductRepository(self.db).get_product_by_id(id=price_update.product_id)
        
        if not product_id_exists:
            logger.info("El producto no existe en base de datos")
            return ServiceResult(ProductExceptions.ProductNotFoundException())
        
        if price_update.price <= 0:
            logger.info("El precio debe ser mayor a 0")
            return ServiceResult(PriceExceptions.LowPriceException())

        product_id_exists_in_price = await PriceRepository(self.db).get_price_by_product_id(product_id=price_update.product_id)
        
        if product_id_exists_in_price and product_id_exists_in_price.id != id:
            logger.info("El producto ya tiene un precio asignado")
            return ServiceResult(PriceExceptions.PriceProductExistsException())

        try:
            price = await PriceRepository(self.db).update_price(
                id=id,
                price_update=price_update,
                updated_by_id=current_user.id,
            )

            if isinstance(price, dict) and not price.get("id"):
                logger.info("The price ID to update is not in the database")
                return ServiceResult(PriceExceptions.PriceNotFoundException())

            return ServiceResult(PriceInDB(**price.dict()))

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return ServiceResult(PriceExceptions.PriceInvalidUpdateParamsException(e))
    
    async def delete_price_by_id(
        self, id: UUID
    ) -> ServiceResult:
        
        price_id = await PriceRepository(self.db).delete_price_by_id(id=id)

        if isinstance(price_id, dict) and not price_id.get("id"):
            logger.info("The price ID to delete is not in the database")
            return ServiceResult(PriceExceptions.PriceNotFoundException())
        
        return ServiceResult(price_id)