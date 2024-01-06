from modules.raw_material.raw_material_repositories import RawMaterialRepository
from modules.supplier.supplier_repositories import SupplierRepository
from modules.price.price_repositories import PriceRepository
from databases import Database
from loguru import logger
from typing import List
from uuid import UUID

from modules.purchase.purchase_exceptions import PurchaseExceptions
from modules.purchase.purchase_schemas import (
    PurchaseInDB,
    PurchaseToSave,
    PurchaseUpdate
)

from shared.utils.record_to_dict import record_to_dict
import shared.utils.repository_utils as ru

class PurchaseRepository:
    def __init__(self, db: Database):
        self.db = db
        
    async def get_complete_purchase(self, record):
        purchase = PurchaseInDB(**dict(record))
        if (purchase.supplier_id):
            supplier = await SupplierRepository(self.db).get_supplier_by_id(purchase.supplier_id)
            if supplier:
                purchase.supplier = supplier
            else:
                raise PurchaseExceptions.PurchaseCreateException()
        
        if (purchase.raw_material_id):
            raw_material = await RawMaterialRepository(self.db).get_raw_material_by_id(purchase.raw_material_id)
            if raw_material:
                purchase.raw_material = raw_material
            else:
                raise PurchaseExceptions.PurchaseCreateException()        
        
        return purchase
    
    async def create_purchase(self, purchase: PurchaseToSave) -> PurchaseInDB:
        from modules.purchase.purchase_sqlstatements import CREATE_PURCHASE_ITEM

        values = ru.preprocess_create(purchase.dict())
        record = await self.db.fetch_one(query=CREATE_PURCHASE_ITEM, values=values)

        return await self.get_complete_purchase(record_to_dict(record))

    
    async def get_purchase_list(
        self,
        search: str | None,
        order: str | None,
        direction: str | None,
    ) -> List:
        from modules.purchase.purchase_sqlstatements import (
            GET_PURCHASE_LIST,
            purchase_list_complements,
            purchase_list_search,
        )

        order = order.lower() if order != None else None
        direction = direction.upper() if order != None else None
        values = {}
        sql_sentence = purchase_list_complements(order, direction)
        sql_search = purchase_list_search()

        if not search:
            sql_sentence = GET_PURCHASE_LIST + sql_sentence
        else:
            sql_sentence = GET_PURCHASE_LIST + sql_search + sql_sentence
            values["search"] = "%" + search + "%"

        records = await self.db.fetch_all(query=sql_sentence, values=values)

        if len(records) == 0 or not records:
            return []
        
        return [await self.get_complete_purchase(record) for record in records]
    
    async def get_purchase_by_id(self, id: UUID) -> PurchaseInDB | dict:
        from modules.purchase.purchase_sqlstatements import GET_PURCHASE_BY_ID

        values = {"id": id}
        record = await self.db.fetch_one(query=GET_PURCHASE_BY_ID, values=values)
        if not record:
            return {}

        return await self.get_complete_purchase(record_to_dict(record))

    
    async def update_purchase(
        self,
        id: UUID,
        purchase_update: PurchaseUpdate,
        updated_by_id: UUID,
    ) -> PurchaseInDB | dict:
        from modules.purchase.purchase_sqlstatements import UPDATE_PURCHASE_BY_ID

        purchase = await self.get_purchase_by_id(id=id)
        if not purchase:
            return {}

        purchase_update_params = purchase.copy(update=purchase_update.dict(exclude_unset=True))
            
        purchase_params_dict = dict(purchase_update_params)
        purchase_params_dict["updated_by"] = updated_by_id
        purchase_params_dict["updated_at"] = ru._preprocess_date()
        
        if "raw_material" in purchase_params_dict:
            del purchase_params_dict["raw_material"]
        
        if "supplier" in purchase_params_dict:
            del purchase_params_dict["supplier"]
        
        try:
            record = await self.db.fetch_one(query=UPDATE_PURCHASE_BY_ID, values=purchase_params_dict)
            purchase_updated = record_to_dict(record)
            return await self.get_purchase_by_id(id=purchase_updated.get("id"))
        except Exception as e:
            logger.error(f"Datos inválidos para actualizar una compra: {e}")
            raise PurchaseExceptions.PurchaseInvalidUpdateParamsException()
        
    async def delete_purchase_by_id(
        self,
        id: UUID,
    ) -> UUID | dict:
        from modules.purchase.purchase_sqlstatements import DELETE_PURCHASE_BY_ID

        purchase = await self.get_purchase_by_id(id=id)

        if not purchase:
            return {}
        
        record = await self.db.fetch_one(query= DELETE_PURCHASE_BY_ID, values = {"id": id})
        purchase_id_delete = dict(record)        

        return purchase_id_delete
