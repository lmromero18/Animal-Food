from modules.warehouse.warehouse_repositories import WarehouseRepository
from databases import Database
from loguru import logger
from typing import List
from uuid import UUID

from modules.raw_material.raw_material_exceptions import RawMaterialExceptions
from modules.raw_material.raw_material_schemas import (
    RawMaterialCreate,
    RawMaterialInDB,
    RawMaterialToSave,
    RawMaterialUpdate
)

from shared.utils.record_to_dict import record_to_dict
import shared.utils.repository_utils as ru

class RawMaterialRepository:
    def __init__(self, db: Database):
        self.db = db
        
    async def get_complete_raw_material(self, record):
        raw_material = RawMaterialInDB(**dict(record))
        if (raw_material.warehouse_id):            
            warehouse = await WarehouseRepository(self.db).get_warehouse_by_id(raw_material.warehouse_id)
            if warehouse:
                raw_material.warehouse = warehouse
            else:
                raise RawMaterialExceptions.RawMaterialInvalidWarehouseIdException()
        return raw_material

    async def create_raw_material(self, raw_material: RawMaterialToSave) -> RawMaterialInDB:
        from modules.raw_material.raw_material_sqlstatements import CREATE_RAW_MATERIAL_ITEM

        values = ru.preprocess_create(raw_material.dict())
        record = await self.db.fetch_one(query=CREATE_RAW_MATERIAL_ITEM, values=values)

        result = record_to_dict(record)

        return await self.get_complete_raw_material(result)
    
    async def get_raw_material_list(
        self,
        search: str | None,
        order: str | None,
        direction: str | None,
    ) -> List[RawMaterialInDB]:
        from modules.raw_material.raw_material_sqlstatements import (
            GET_RAW_MATERIAL_LIST,
            raw_material_list_complements,
            raw_material_list_search,
        )

        order = order.lower() if order else None
        direction = direction.upper() if direction else None
        values = {}
        sql_sentence = raw_material_list_complements(order, direction)
        sql_search = raw_material_list_search()

        if not search:
            sql_sentence = GET_RAW_MATERIAL_LIST + sql_sentence
        else:
            sql_sentence = GET_RAW_MATERIAL_LIST + sql_search + sql_sentence
            values["search"] = "%" + search + "%"

        records = await self.db.fetch_all(query=sql_sentence, values=values)

        if not records:
            return []
        
        return [await self.get_complete_raw_material(record_to_dict(record)) for record in records]
    
    async def get_raw_material_by_id(self, id: UUID) -> RawMaterialInDB | dict:
        from modules.raw_material.raw_material_sqlstatements import GET_RAW_MATERIAL_BY_ID

        values = {"id": id}
        record = await self.db.fetch_one(query=GET_RAW_MATERIAL_BY_ID, values=values)
        if not record:
            return {}

        raw_material = record_to_dict(record)
        return RawMaterialInDB(**raw_material)
    
    async def update_raw_material(
        self,
        id: UUID,
        raw_material_update: RawMaterialUpdate,
        updated_by_id: UUID,
    ) -> RawMaterialInDB | dict:
        from modules.raw_material.raw_material_sqlstatements import UPDATE_RAW_MATERIAL_BY_ID

        raw_material = await self.get_raw_material_by_id(id=id)
        if not raw_material:
            return {}

        raw_material_update_params = raw_material.copy(update=raw_material_update.dict(exclude_unset=True))

        raw_material_params_dict = raw_material_update_params.dict()
        raw_material_params_dict["updated_by"] = updated_by_id
        raw_material_params_dict["updated_at"] = ru._preprocess_date()
        
           #Si viene warehouse eliminarlo del diccionario para que no se actualice
        if "warehouse" in raw_material_params_dict:
            del raw_material_params_dict["warehouse"]
        
        try:
            record = await self.db.fetch_one(query=UPDATE_RAW_MATERIAL_BY_ID, values=raw_material_params_dict)
            raw_material_updated = record_to_dict(record)
            return await self.get_raw_material_by_id(id=raw_material_updated.get("id"))
        except Exception as e:
            logger.error(f"Datos inválidos para actualizar una materia prima: {e}")
            raise RawMaterialExceptions.RawMaterialInvalidUpdateParamsException()
        
    async def delete_raw_material_by_id(
        self,
        id: UUID,
    ) -> UUID | dict:
        from modules.raw_material.raw_material_sqlstatements import DELETE_RAW_MATERIAL_BY_ID

        raw_material = await self.get_raw_material_by_id(id=id)

        if not raw_material:
            return {}
        
        record = await self.db.fetch_one(query=DELETE_RAW_MATERIAL_BY_ID, values={"id": id})
        raw_material_id_delete = dict(record)        

        return raw_material_id_delete