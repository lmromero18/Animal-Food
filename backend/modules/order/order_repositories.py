from datetime import datetime
from decimal import Decimal
from modules.product_offered.product_offered_exceptions import ProductOfferedExceptions
from modules.product_offered.product_offered_repositories import ProductOfferedRepository
from modules.raw_material.raw_material_repositories import RawMaterialRepository
from modules.supplier.supplier_repositories import SupplierRepository
from modules.price.price_repositories import PriceRepository
from databases import Database
from loguru import logger
from typing import List
from uuid import UUID

from modules.order.order_exceptions import OrderExceptions
from modules.order.order_schemas import (
    OrderInDB,
    OrderToSave,
    OrderUpdate
)

from shared.utils.record_to_dict import record_to_dict
import shared.utils.repository_utils as ru

class OrderRepository:
    def __init__(self, db: Database):
        self.db = db
        
    async def get_complete_order(self, record):
        order = OrderInDB(**dict(record))
        if order.product_offered_id:
            order.product_offered = await ProductOfferedRepository(self.db).get_product_offered_by_id(id=order.product_offered_id)
        
        return order
    
    async def create_order(self, order: OrderToSave) -> OrderInDB:
        from modules.order.order_sqlstatements import CREATE_ORDER_ITEM

        values = ru.preprocess_create(order.dict())
        record = await self.db.fetch_one(query=CREATE_ORDER_ITEM, values=values)

        return await self.get_complete_order(record_to_dict(record))

    
    async def get_order_list(
        self,
        search: str | None,
        order: str | None,
        direction: str | None,
    ) -> List:
        from modules.order.order_sqlstatements import (
            GET_ORDER_LIST,
            order_list_complements,
            order_list_search,
        )

        order = order.lower() if order != None else None
        direction = direction.upper() if order != None else None
        values = {}
        sql_sentence = order_list_complements(order, direction)
        sql_search = order_list_search()

        if not search:
            sql_sentence = GET_ORDER_LIST + sql_sentence
        else:
            sql_sentence = GET_ORDER_LIST + sql_search + sql_sentence
            values["search"] = "%" + search + "%"

        records = await self.db.fetch_all(query=sql_sentence, values=values)

        if len(records) == 0 or not records:
            return []
        
        return [await self.get_complete_order(record) for record in records]
    
    async def get_order_by_id(self, id: UUID) -> OrderInDB | dict:
        from modules.order.order_sqlstatements import GET_ORDER_BY_ID

        values = {"id": id}
        record = await self.db.fetch_one(query=GET_ORDER_BY_ID, values=values)
        if not record:
            return {}

        return await self.get_complete_order(record_to_dict(record))

    
    async def update_order(
        self,
        id: UUID,
        order_update: OrderUpdate,
        updated_by_id: UUID,
    ) -> OrderInDB | dict:
        from modules.order.order_sqlstatements import UPDATE_ORDER_BY_ID

        order = await self.get_order_by_id(id=id)
        if not order:
            return {}
        
        previous_discount = order.discount
        order_update_params = order.copy(update=order_update.dict(exclude_unset=True))
            
        order_params_dict = dict(order_update_params)
        order_params_dict["updated_by"] = updated_by_id
        order_params_dict["updated_at"] = ru._preprocess_date()  
        
        # Compara el descuento anterior con el nuevo descuento
        if previous_discount != order_params_dict["discount"]:
            # Si son diferentes, actualiza el total
            product_item = await ProductOfferedRepository(self.db).get_product_offered_by_id(id=order_update.product_offered_id)
            order_params_dict["total"] = (product_item.product.price.price * order_params_dict["quantity"]) - order_params_dict["discount"]
            
        # Si el pedido se marca como entregado, actualiza la fecha de entrega                 
        if (order_params_dict["is_delivered"] == True):
            order_params_dict["delivery_date"] = datetime.now()
            product_offered = await ProductOfferedRepository(self.db).get_product_offered_by_id(id=order_update.product_offered_id)
            if product_offered:
                quantity = int(order_params_dict["quantity"])
                product_offered.quantity -= quantity
                if "warehouse" in product_offered:
                    del product_offered["warehouse"]
                    
                if "product" in product_offered:
                    del product_offered["product"]
                
                await ProductOfferedRepository(self.db).update_product_offered(id=order_update.product_offered_id, product_offered_update=product_offered, updated_by_id=updated_by_id)
            else:
                raise ProductOfferedExceptions.ProductOfferedInvalidUpdateParamsException() 

        # Elimina el campo product_offered para que no se actualice
        if "product_offered" in order_params_dict:
            del order_params_dict["product_offered"]

        try:
            record = await self.db.fetch_one(query=UPDATE_ORDER_BY_ID, values=order_params_dict)
            order_updated = record_to_dict(record)
            return await self.get_order_by_id(id=order_updated.get("id"))
        except Exception as e:
            logger.error(f"Datos inválidos para actualizar un pedido: {e}")
            raise OrderExceptions.OrderInvalidUpdateParamsException()
        
    async def delete_order_by_id(
        self,
        id: UUID,
    ) -> UUID | dict:
        from modules.order.order_sqlstatements import DELETE_ORDER_BY_ID

        order = await self.get_order_by_id(id=id)

        if not order:
            return {}
        
        record = await self.db.fetch_one(query= DELETE_ORDER_BY_ID, values = {"id": id})
        order_id_delete = dict(record)        

        return order_id_delete
