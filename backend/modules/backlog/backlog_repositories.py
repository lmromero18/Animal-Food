from datetime import datetime
from modules.product.product_repositories import ProductRepository
from databases import Database
from loguru import logger
from typing import List
from uuid import UUID

from modules.backlog.backlog_exceptions import BacklogExceptions
from modules.backlog.backlog_schemas import (
    BacklogInDB,
    BacklogToSave,
    BacklogUpdate
)

from shared.utils.record_to_dict import record_to_dict
import shared.utils.repository_utils as ru

class BacklogRepository:
    def __init__(self, db: Database):
        self.db = db

    async def get_complete_backlog(self, record):
        backlog = BacklogInDB(**dict(record))
        if backlog.product_id:
            backlog.product = await ProductRepository(self.db).get_product_by_id(id=backlog.product_id)
        
        return backlog


    async def create_backlog(self, backlog: BacklogToSave) -> BacklogInDB:
        from modules.backlog.backlog_sqlstatements import CREATE_BACKLOG_ITEM

        values = ru.preprocess_create(backlog.dict())
        record = await self.db.fetch_one(query=CREATE_BACKLOG_ITEM, values=values)

        return await self.get_complete_backlog(record_to_dict(record))
    
    async def get_backlog_list(
        self,
        search: str | None,
        order: str | None,
        direction: str | None,
    ) -> List:
        from modules.backlog.backlog_sqlstatements import (
            GET_BACKLOG_LIST,
            backlog_list_complements,
            backlog_list_search,
        )

        order = order.lower() if order != None else None
        direction = direction.upper() if order != None else None
        values = {}
        sql_sentence = backlog_list_complements(order, direction)
        sql_search = backlog_list_search()

        if not search:
            sql_sentence = GET_BACKLOG_LIST + sql_sentence
        else:
            sql_sentence = GET_BACKLOG_LIST + sql_search + sql_sentence
            values["search"] = "%" + search + "%"

        records = await self.db.fetch_all(query=sql_sentence, values=values)

        if len(records) == 0 or not records:
            return []
        
        return [await self.get_complete_backlog(record) for record in records]
    
    async def get_backlog_by_id(self, id: UUID) -> BacklogInDB | dict:
        from modules.backlog.backlog_sqlstatements import GET_BACKLOG_BY_ID

        values = {"id": id}
        record = await self.db.fetch_one(query=GET_BACKLOG_BY_ID, values=values)
        if not record:
            return {}

        return await self.get_complete_backlog(record_to_dict(record))
    
    async def update_backlog(
        self,
        id: UUID,
        backlog_update: BacklogUpdate,
        updated_by_id: UUID,
    ) -> BacklogInDB | dict:
        from modules.backlog.backlog_sqlstatements import UPDATE_BACKLOG_BY_ID

        backlog = await self.get_backlog_by_id(id=id)
        if not backlog:
            return {}

        backlog_update_params = backlog.copy(update=backlog_update.dict(exclude_unset=True))

        backlog_params_dict = backlog_update_params.dict()
        backlog_params_dict["updated_by"] = updated_by_id
        backlog_params_dict["updated_at"] = ru._preprocess_date()
        
        if "product" in backlog_params_dict:
            del backlog_params_dict["product"]
        
        try:
            record = await self.db.fetch_one(query=UPDATE_BACKLOG_BY_ID, values=backlog_params_dict)
            backlog_updated = record_to_dict(record)
            return await self.get_backlog_by_id(id=backlog_updated.get("id"))
        except Exception as e:
            logger.error(f"Datos inválidos para actualizar un backlog: {e}")
            raise BacklogExceptions.BacklogInvalidUpdateParamsException()
        
    async def delete_backlog_by_id(
        self,
        id: UUID,
    ) -> UUID | dict:
        from modules.backlog.backlog_sqlstatements import DELETE_BACKLOG_BY_ID

        backlog = await self.get_backlog_by_id(id=id)

        if not backlog:
            return {}
        
        record = await self.db.fetch_one(query= DELETE_BACKLOG_BY_ID, values = {"id": id})
        backlog_id_delete = dict(record)        

        return backlog_id_delete

    async def get_backlog_by_product_id(self, product_id: UUID) -> BacklogInDB | dict:
        from modules.backlog.backlog_sqlstatements import GET_BACKLOG_BY_PRODUCT_ID

        values = {"product_id": product_id}
        record = await self.db.fetch_one(query=GET_BACKLOG_BY_PRODUCT_ID, values=values)
        if not record:
            return {}

        return await self.get_complete_backlog(record_to_dict(record))
    
    async def update_backlog_by_product_id(
        self,
        product_id: UUID,
        quantity: int,
        updated_by_id: UUID,
    ) -> List[BacklogInDB] | dict:
        from modules.backlog.backlog_sqlstatements import GET_BACKLOG_BY_PRODUCT_ID, UPDATE_BACKLOG_BY_PRODUCT_ID

        backlogs = await self.db.fetch_all(query=GET_BACKLOG_BY_PRODUCT_ID, values={"product_id": product_id})

        if not backlogs:
            return {}

        updated_backlogs = []
        for record in backlogs:
            backlog = dict(record)
            if quantity > 0:
                if backlog["required_quantity"] > quantity:
                    backlog["required_quantity"] -= quantity
                    quantity = 0
                else:
                    quantity -= backlog["required_quantity"]
                    backlog["required_quantity"] = 0
                    backlog["is_active"] = False

                backlog["updated_by"] = updated_by_id
                backlog["updated_at"] = datetime.now()

                updated_backlog = await self.db.fetch_one(query=UPDATE_BACKLOG_BY_PRODUCT_ID, values=backlog)
                updated_backlogs.append(updated_backlog)

        return updated_backlogs

