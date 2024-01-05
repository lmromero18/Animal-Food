from modules.product.product_repositories import ProductRepository
from modules.warehouse.warehouse_repositories import WarehouseRepository
from databases import Database
from loguru import logger
from typing import List
from uuid import UUID

from modules.product_offered.product_offered_exceptions import ProductOfferedExceptions
from modules.product_offered.product_offered_schemas import (
    ProductOfferedCreate,
    ProductOfferedInDB,
    ProductOfferedToSave,
    ProductOfferedUpdate
)

from shared.utils.record_to_dict import record_to_dict
import shared.utils.repository_utils as ru

class ProductOfferedRepository:
    def __init__(self, db: Database):
        self.db = db
        
    async def get_complete_product_offered(self, record):
        product_offered = ProductOfferedInDB(**dict(record))
        if (product_offered.warehouse_id):            
            warehouse = await WarehouseRepository(self.db).get_warehouse_by_id(product_offered.warehouse_id)
            if warehouse:
                product_offered.warehouse = warehouse
            else:
                raise ProductOfferedExceptions.ProductOfferedInvalidWarehouseIdException()
            
        if (product_offered.product_id):            
            product = await ProductRepository(self.db).get_product_by_id(product_offered.product_id)
            if product:
                product_offered.product = product
            else:
                raise ProductOfferedExceptions.ProductOfferedInvalidProductIdException()
        return product_offered
    
    async def create_product_offered(self, product_offered: ProductOfferedToSave) -> ProductOfferedInDB:
        from modules.product_offered.product_offered_sqlstatements import CREATE_PRODUCT_OFFERED_ITEM

        values = ru.preprocess_create(product_offered.dict())
        record = await self.db.fetch_one(query=CREATE_PRODUCT_OFFERED_ITEM, values=values)

        return await self.get_complete_product_offered(record_to_dict(record))

    
    async def get_product_offered_list(
        self,
        search: str | None,
        order: str | None,
        direction: str | None,
    ) -> List:
        from modules.product_offered.product_offered_sqlstatements import (
            GET_PRODUCT_OFFERED_LIST,
            product_offered_list_complements,
            product_offered_list_search,
        )

        order = order.lower() if order != None else None
        direction = direction.upper() if order != None else None
        values = {}
        sql_sentence = product_offered_list_complements(order, direction)
        sql_search = product_offered_list_search()

        if not search:
            sql_sentence = GET_PRODUCT_OFFERED_LIST + sql_sentence
        else:
            sql_sentence = GET_PRODUCT_OFFERED_LIST + sql_search + sql_sentence
            values["search"] = "%" + search + "%"

        records = await self.db.fetch_all(query=sql_sentence, values=values)

        if len(records) == 0 or not records:
            return []
        
        return [await self.get_complete_product_offered(record) for record in records]
    
    async def get_product_offered_by_id(self, id: UUID) -> ProductOfferedInDB | dict:
        from modules.product_offered.product_offered_sqlstatements import GET_PRODUCT_OFFERED_BY_ID

        values = {"id": id}
        record = await self.db.fetch_one(query=GET_PRODUCT_OFFERED_BY_ID, values=values)
        if not record:
            return {}

        return await self.get_complete_product_offered(record_to_dict(record))

    
    async def update_product_offered(
        self,
        id: UUID,
        product_offered_update: ProductOfferedUpdate,
        updated_by_id: UUID,
    ) -> ProductOfferedInDB | dict:
        from modules.product_offered.product_offered_sqlstatements import UPDATE_PRODUCT_OFFERED_BY_ID

        product_offered = await self.get_product_offered_by_id(id=id)
        if not product_offered:
            return {}

        product_offered_update_params = product_offered.copy(update=product_offered_update.dict(exclude_unset=True))
            
        product_offered_params_dict = dict(product_offered_update_params)
        product_offered_params_dict["updated_by"] = updated_by_id
        product_offered_params_dict["updated_at"] = ru._preprocess_date()        
        
        # If warehouse is present, remove it from the dictionary so that it is not updated
        if "warehouse" in product_offered_params_dict:
            del product_offered_params_dict["warehouse"]
        
        # If product is present, remove it from the dictionary so that it is not updated  
        if "product" in product_offered_params_dict:
            del product_offered_params_dict["product"]
        
        try:
            record = await self.db.fetch_one(query=UPDATE_PRODUCT_OFFERED_BY_ID, values=product_offered_params_dict)
            product_offered_updated = record_to_dict(record)
            return await self.get_product_offered_by_id(id=product_offered_updated.get("id"))
        except Exception as e:
            logger.error(f"Invalid data to update a product offered: {e}")
            raise ProductOfferedExceptions.ProductOfferedInvalidUpdateParamsException()
        
    async def delete_product_offered_by_id(
        self,
        id: UUID,
    ) -> UUID | dict:
        from modules.product_offered.product_offered_sqlstatements import DELETE_PRODUCT_OFFERED_BY_ID

        product_offered = await self.get_product_offered_by_id(id=id)

        if not product_offered:
            return {}
        
        record = await self.db.fetch_one(query=DELETE_PRODUCT_OFFERED_BY_ID, values={"id": id})
        product_offered_id_delete = dict(record)        

        return product_offered_id_delete