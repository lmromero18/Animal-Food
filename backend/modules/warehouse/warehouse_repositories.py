from databases import Database
from loguru import logger
from typing import List
from uuid import UUID

from modules.warehouse.warehouse_exceptions import WarehouseExceptions
from modules.warehouse.warehouse_schemas import (
    WarehouseInDB,
    WarehouseToSave,
    WarehouseUpdate
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
    
    async def get_warehouse_list(
        self,
        search: str | None,
        order: str | None,
        direction: str | None,
    ) -> List:
        from modules.warehouse.warehouse_sqlstatements import (
            GET_WAREHOUSE_LIST,
            warehouse_list_complements,
            warehouse_list_search,
        )

        order = order.lower() if order != None else None
        direction = direction.upper() if order != None else None
        values = {}
        sql_sentence = warehouse_list_complements(order, direction)
        sql_search = warehouse_list_search()

        if not search:
            sql_sentence = GET_WAREHOUSE_LIST + sql_sentence
        else:
            sql_sentence = GET_WAREHOUSE_LIST + sql_search + sql_sentence
            values["search"] = "%" + search + "%"

        records = await self.db.fetch_all(query=sql_sentence, values=values)

        if len(records) == 0 or not records:
            return []
        
        return [WarehouseInDB(**dict(record)) for record in records] 
    
    async def get_warehouse_by_id(self, id: UUID) -> WarehouseInDB | dict:
        from modules.warehouse.warehouse_sqlstatements import GET_WAREHOUSE_BY_ID

        values = {"id": id}
        record = await self.db.fetch_one(query=GET_WAREHOUSE_BY_ID, values=values)
        if not record:
            return {}

        warehouse = record_to_dict(record)
        return WarehouseInDB(**warehouse)
    
    async def update_warehouse(
        self,
        id: UUID,
        warehouse_update: WarehouseUpdate,
        updated_by_id: UUID,
    ) -> WarehouseInDB | dict:
        from modules.warehouse.warehouse_sqlstatements import UPDATE_WAREHOUSE_BY_ID

        warehouse = await self.get_warehouse_by_id(id=id)
        if not warehouse:
            return {}

        warehouse_update_params = warehouse.copy(update=warehouse_update.dict(exclude_unset=True))

        warehouse_params_dict = warehouse_update_params.dict()
        warehouse_params_dict["updated_by"] = updated_by_id
        warehouse_params_dict["updated_at"] = ru._preprocess_date()
        
        try:
            record = await self.db.fetch_one(query=UPDATE_WAREHOUSE_BY_ID, values=warehouse_params_dict)
            warehouse_updated = record_to_dict(record)
            return await self.get_warehouse_by_id(id=warehouse_updated.get("id"))
        except Exception as e:
            logger.error(f"Datos inválidos para actualizar un almacén: {e}")
            raise WarehouseExceptions.WarehouseInvalidUpdateParamsException()
        
    async def delete_warehouse_by_id(
        self,
        id: UUID,
    ) -> UUID | dict:
        from modules.warehouse.warehouse_sqlstatements import DELETE_WAREHOUSE_BY_ID

        warehouse = await self.get_warehouse_by_id(id=id)

        if not warehouse:
            return {}
        
        record = await self.db.fetch_one(query= DELETE_WAREHOUSE_BY_ID, values = {"id": id})
        warehouse_id_delete = dict(record)        

        return warehouse_id_delete
