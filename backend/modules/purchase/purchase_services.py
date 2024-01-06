from datetime import datetime
from typing import List
from uuid import UUID
import uuid
from shared.utils.record_to_dict import record_to_dict
from shared.utils.verify_uuid import is_valid_uuid

from databases import Database
import fastapi
from loguru import logger

from shared.utils.service_result import ServiceResult   
from modules.purchase.purchase_repositories import PurchaseRepository
from modules.purchase.purchase_exceptions import PurchaseExceptions
from modules.purchase.purchase_schemas import (
    PurchaseCreate,
    PurchaseToSave,
    PurchaseInDB,
    PurchaseUpdate
)
from modules.users.users.user_schemas import UserInDB
from shared.core.config import API_PREFIX
import shared.utils.repository_utils as ru
from shared.utils.short_pagination import short_pagination

class PurchaseService:
    def __init__(self, db: Database):
        self.db = db
  
    async def create_purchase(
        self, purchase: PurchaseCreate, current_user: UserInDB):

        new_purchase = PurchaseToSave(**purchase.dict())
        new_purchase.is_delivered = False
        new_purchase.order_date = datetime.now()
        new_purchase.created_by = current_user.id
        new_purchase.updated_by = uuid.UUID(int=0)

        purchase_item = await PurchaseRepository(self.db).create_purchase(new_purchase)

        if not purchase_item:
            logger.error("Error creating purchase")
            return ServiceResult(PurchaseExceptions.PurchaseCreateException())

        return ServiceResult(purchase_item)
    
    async def get_purchase_list(
        self,
        search: str | None,
        page_num: int = 1,
        page_size: int = 10,
        order: str = None,
        direction: str = None,
    ) -> ServiceResult:
        purchases = await PurchaseRepository(self.db).get_purchase_list(search, order, direction)

        service_result = None
        if len(purchases) == 0:
            service_result = ServiceResult([])
            service_result.status_code = 204
        else:
            response = short_pagination(
                page_num=page_num,
                page_size=page_size,
                data_list=purchases,
                route=f"{API_PREFIX}/purchases",
            )
            service_result = ServiceResult(response)

        return service_result
    
    async def get_purchase_by_id(self, id: UUID) -> ServiceResult:
        purchase_in_db = await PurchaseRepository(self.db).get_purchase_by_id(id=id)

        if isinstance(purchase_in_db, dict) and not purchase_in_db.get("id"):
            logger.info("La compra solicitada no está en base de datos")
            return ServiceResult(PurchaseExceptions.PurchaseNotFoundException())

        purchase = PurchaseInDB(**purchase_in_db.dict())
        return ServiceResult(purchase)
    
    async def update_purchase(
        self, id: UUID, purchase_update: PurchaseUpdate, current_user: UserInDB
    ) -> ServiceResult:
        if not is_valid_uuid(id):
            return ServiceResult(PurchaseExceptions.PurchaseIdNoValidException())

        try:
            purchase = await PurchaseRepository(self.db).update_purchase(
                id=id,
                purchase_update=purchase_update,
                updated_by_id=current_user.id,
            )

            if isinstance(purchase, dict) and not purchase.get("id"):
                logger.info("El ID de la compra a actualizar no está en base de datos")
                return ServiceResult(PurchaseExceptions.PurchaseNotFoundException())

            return ServiceResult(PurchaseInDB(**purchase.dict()))

        except Exception as e:
            logger.error(f"Error: {e}")
            return ServiceResult(PurchaseExceptions.PurchaseInvalidUpdateParamsException(e))
    
    async def delete_purchase_by_id(
        self, id: UUID
    ) -> ServiceResult:
        
        purchase_id = await PurchaseRepository(self.db).delete_purchase_by_id(id=id)

        if isinstance(purchase_id, dict) and not purchase_id.get("id"):
            logger.info("El ID de la compra a eliminar no está en base de datos")
            return ServiceResult(PurchaseExceptions.PurchaseNotFoundException())
        
        return ServiceResult(purchase_id)
