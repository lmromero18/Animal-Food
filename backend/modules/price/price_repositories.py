from modules.product.product_repositories import ProductRepository
from modules.warehouse.warehouse_repositories import WarehouseRepository
from databases import Database
from loguru import logger
from typing import List
from uuid import UUID

from modules.price.price_exceptions import PriceExceptions
from modules.price.price_schemas import (
PriceCreate,
PriceInDB,
PriceToSave,
PriceUpdate
)

from shared.utils.record_to_dict import record_to_dict
import shared.utils.repository_utils as ru

class PriceRepository:
    def __init__(self, db: Database):
        self.db = db
        
    async def get_complete_price(self, record):
        price = PriceInDB(**dict(record))
        if (price.product_id):            
            product = await ProductRepository(self.db).get_product_by_id(price.product_id)
            if product:
                price.product = product
            else:
                raise PriceExceptions.PriceCreateException()
        return price    
        
    async def create_price(self, price: PriceToSave) -> PriceInDB:
        from modules.price.price_sqlstatements import CREATE_PRICE_ITEM

        values = ru.preprocess_create(price.dict())
        record = await self.db.fetch_one(query=CREATE_PRICE_ITEM, values=values)

        result = record_to_dict(record)

        return await self.get_complete_price(result)

    async def get_price_list(
        self,
        search: str | None,
        order: str | None,
        direction: str | None,
    ) -> List[PriceInDB]:
        from modules.price.price_sqlstatements import (
            GET_PRICE_LIST,
            price_list_complements,
            price_list_search,
        )

        order = order.lower() if order else None
        direction = direction.upper() if direction else None
        values = {}
        sql_sentence = price_list_complements(order, direction)
        sql_search = price_list_search()

        if not search:
            sql_sentence = GET_PRICE_LIST + sql_sentence
        else:
            sql_sentence = GET_PRICE_LIST + sql_search + sql_sentence
            values["search"] = "%" + search + "%"

        records = await self.db.fetch_all(query=sql_sentence, values=values)

        if not records:
            return []
        
        return [await self.get_complete_price(record_to_dict(record)) for record in records]

    async def get_price_by_id(self, id: UUID) -> PriceInDB | dict:
        from modules.price.price_sqlstatements import GET_PRICE_BY_ID

        values = {"id": id}
        record = await self.db.fetch_one(query=GET_PRICE_BY_ID, values=values)
        if not record:
            return {}

        return await self.get_complete_price(record_to_dict(record))

    async def update_price(
        self,
        id: UUID,
        price_update: PriceUpdate,
        updated_by_id: UUID,
    ) -> PriceInDB | dict:
        from modules.price.price_sqlstatements import UPDATE_PRICE_BY_ID

        price = await self.get_price_by_id(id=id)
        if not price:
            return {}

        price_update_params = price.copy(update=price_update.dict(exclude_unset=True))

        price_params_dict = price_update_params.dict()
        price_params_dict["updated_by"] = updated_by_id
        price_params_dict["updated_at"] = ru._preprocess_date()
        
        if "product" in price_params_dict:
            del price_params_dict["product"]
        
        try:
            record = await self.db.fetch_one(query=UPDATE_PRICE_BY_ID, values=price_params_dict)
            price_updated = record_to_dict(record)
            return await self.get_price_by_id(id=price_updated.get("id"))
        except Exception as e:
            logger.error(f"Datos inválidos para actualizar un precio: {e}")
            raise PriceExceptions.PriceInvalidUpdateParamsException()
        
    async def delete_price_by_id(
        self,
        id: UUID,
    ) -> UUID | dict:
        from modules.price.price_sqlstatements import DELETE_PRICE_BY_ID

        price = await self.get_price_by_id(id=id)

        if not price:
            return {}
        
        record = await self.db.fetch_one(query=DELETE_PRICE_BY_ID, values={"id": id})
        price_id_delete = dict(record)        

        return price_id_delete
    
    async def get_price_by_product_id(self, product_id: UUID) -> PriceInDB | dict:
        from modules.price.price_sqlstatements import GET_PRICE_BY_PRODUCT_ID

        values = {"product_id": product_id}
        record = await self.db.fetch_one(query=GET_PRICE_BY_PRODUCT_ID, values=values)
        if not record:
            return {}

        return await self.get_complete_price(record_to_dict(record))