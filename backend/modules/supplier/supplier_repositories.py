from modules.warehouse.warehouse_repositories import WarehouseRepository
from databases import Database
from loguru import logger
from typing import List
from uuid import UUID

from modules.supplier.supplier_exceptions import SupplierExceptions
from modules.supplier.supplier_schemas import (
SupplierCreate,
SupplierInDB,
SupplierToSave,
SupplierUpdate
)

from shared.utils.record_to_dict import record_to_dict
import shared.utils.repository_utils as ru

class SupplierRepository:
    def __init__(self, db: Database):
        self.db = db
        
    async def get_complete_supplier(self, record):
        supplier = SupplierInDB(**dict(record))
        return supplier

    async def create_supplier(self, supplier: SupplierToSave) -> SupplierInDB:
        from modules.supplier.supplier_sqlstatements import CREATE_SUPPLIER_ITEM

        values = ru.preprocess_create(supplier.dict())
        record = await self.db.fetch_one(query=CREATE_SUPPLIER_ITEM, values=values)

        result = record_to_dict(record)

        return await self.get_complete_supplier(result)

    async def get_supplier_list(
        self,
        search: str | None,
        order: str | None,
        direction: str | None,
    ) -> List[SupplierInDB]:
        from modules.supplier.supplier_sqlstatements import (
            GET_SUPPLIER_LIST,
            supplier_list_complements,
            supplier_list_search,
        )

        order = order.lower() if order else None
        direction = direction.upper() if direction else None
        values = {}
        sql_sentence = supplier_list_complements(order, direction)
        sql_search = supplier_list_search()

        if not search:
            sql_sentence = GET_SUPPLIER_LIST + sql_sentence
        else:
            sql_sentence = GET_SUPPLIER_LIST + sql_search + sql_sentence
            values["search"] = "%" + search + "%"

        records = await self.db.fetch_all(query=sql_sentence, values=values)

        if not records:
            return []
        
        return [await self.get_complete_supplier(record_to_dict(record)) for record in records]

    async def get_supplier_by_id(self, id: UUID) -> SupplierInDB | dict:
        from modules.supplier.supplier_sqlstatements import GET_SUPPLIER_BY_ID

        values = {"id": id}
        record = await self.db.fetch_one(query=GET_SUPPLIER_BY_ID, values=values)
        if not record:
            return {}

        return await self.get_complete_supplier(record_to_dict(record))

    async def update_supplier(
        self,
        id: UUID,
        supplier_update: SupplierUpdate,
        updated_by_id: UUID,
    ) -> SupplierInDB | dict:
        from modules.supplier.supplier_sqlstatements import UPDATE_SUPPLIER_BY_ID

        supplier = await self.get_supplier_by_id(id=id)
        if not supplier:
            return {}

        supplier_update_params = supplier.copy(update=supplier_update.dict(exclude_unset=True))

        supplier_params_dict = supplier_update_params.dict()
        supplier_params_dict["updated_by"] = updated_by_id
        supplier_params_dict["updated_at"] = ru._preprocess_date()
        
        try:
            record = await self.db.fetch_one(query=UPDATE_SUPPLIER_BY_ID, values=supplier_params_dict)
            supplier_updated = record_to_dict(record)
            return await self.get_supplier_by_id(id=supplier_updated.get("id"))
        except Exception as e:
            logger.error(f"Datos inválidos para actualizar un proveedor: {e}")
            raise SupplierExceptions.SupplierInvalidUpdateParamsException()
        
    async def delete_supplier_by_id(
        self,
        id: UUID,
    ) -> UUID | dict:
        from modules.supplier.supplier_sqlstatements import DELETE_SUPPLIER_BY_ID

        supplier = await self.get_supplier_by_id(id=id)

        if not supplier:
            return {}
        
        record = await self.db.fetch_one(query=DELETE_SUPPLIER_BY_ID, values={"id": id})
        supplier_id_delete = dict(record)        

        return supplier_id_delete
