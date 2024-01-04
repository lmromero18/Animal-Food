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
from modules.product.product_repositories import ProductRepository
from modules.product.product_exceptions import ProductExceptions
from modules.product.product_schemas import (
    ProductCreate,
    ProductToSave,
    ProductInDB,
    ProductUpdate
)
from modules.users.users.user_schemas import UserInDB
from shared.core.config import API_PREFIX
import shared.utils.repository_utils as ru
from shared.utils.short_pagination import short_pagination

class ProductService:
    def __init__(self, db: Database):
        self.db = db
  
    async def create_product(
        self, product: ProductCreate, current_user: UserInDB):

        new_product = ProductToSave(**product.dict())
        new_product.created_by = current_user.id
        new_product.updated_by = uuid.UUID(int=0)

        product_item = await ProductRepository(self.db).create_product(new_product)

        if not product_item:
            logger.error("Error creating product")
            return ServiceResult(ProductExceptions.ProductCreateException())

        return ServiceResult(product_item)
    
    async def get_product_list(
        self,
        search: str | None,
        page_num: int = 1,
        page_size: int = 10,
        order: str = None,
        direction: str = None,
    ) -> ServiceResult:
        products = await ProductRepository(self.db).get_product_list(search, order, direction)

        service_result = None
        if len(products) == 0:
            service_result = ServiceResult([])
            service_result.status_code = 204
        else:
            response = short_pagination(
                page_num=page_num,
                page_size=page_size,
                data_list=products,
                route=f"{API_PREFIX}/products",
            )
            service_result = ServiceResult(response)

        return service_result
    
    async def get_product_by_id(self, id: UUID) -> ServiceResult:
        product_in_db = await ProductRepository(self.db).get_product_by_id(id=id)

        if isinstance(product_in_db, dict) and not product_in_db.get("id"):
            logger.info("El producto solicitado no está en base de datos")
            return ServiceResult(ProductExceptions.ProductNotFoundException())

        product = ProductInDB(**product_in_db.dict())
        return ServiceResult(product)
    
    async def update_product(
        self, id: UUID, product_update: ProductUpdate, current_user: UserInDB
    ) -> ServiceResult:
        if not is_valid_uuid(id):
            return ServiceResult(ProductExceptions.ProductIdNoValidException())

        try:
            product = await ProductRepository(self.db).update_product(
                id=id,
                product_update=product_update,
                updated_by_id=current_user.id,
            )

            if isinstance(product, dict) and not product.get("id"):
                logger.info("El ID del producto a actualizar no está en base de datos")
                return ServiceResult(ProductExceptions.ProductNotFoundException())

            return ServiceResult(ProductInDB(**product.dict()))

        except Exception as e:
            logger.error(f"Error: {e}")
            return ServiceResult(ProductExceptions.ProductInvalidUpdateParamsException(e))
    
    async def delete_product_by_id(
        self, id: UUID
    ) -> ServiceResult:
        
        product_id = await ProductRepository(self.db).delete_product_by_id(id=id)

        if isinstance(product_id, dict) and not product_id.get("id"):
            logger.info("El ID del producto a eliminar no está en base de datos")
            return ServiceResult(ProductExceptions.ProductNotFoundException())
        
        return ServiceResult(product_id)