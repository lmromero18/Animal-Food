from datetime import datetime
from typing import List
from uuid import UUID
import uuid
from modules.backlog.backlog_exceptions import BacklogExceptions
from modules.backlog.backlog_schemas import BacklogToSave
from modules.backlog.backlog_repositories import BacklogRepository
from modules.product_offered.product_offered_exceptions import ProductOfferedExceptions
from modules.product_offered.product_offered_repositories import ProductOfferedRepository
from shared.utils.verify_uuid import is_valid_uuid

from databases import Database
import fastapi
from loguru import logger

from shared.utils.service_result import ServiceResult   
from modules.order.order_repositories import OrderRepository
from modules.order.order_exceptions import OrderExceptions
from modules.order.order_schemas import (
    OrderCreate,
    OrderToSave,
    OrderInDB,
    OrderUpdate
)
from modules.users.users.user_schemas import UserInDB
from shared.core.config import API_PREFIX
import shared.utils.repository_utils as ru
from shared.utils.short_pagination import short_pagination

class OrderService:
    def __init__(self, db: Database):
        self.db = db
  
    async def create_order(
        self, order: OrderCreate, current_user: UserInDB):

        new_order = OrderToSave(**order.dict())
        new_order.is_delivered = False        
        new_order.order_date = datetime.now()
        new_order.created_by = current_user.id
        new_order.updated_by = uuid.UUID(int=0)        
               
        
        product_item = await ProductOfferedRepository(self.db).get_product_offered_by_id(id=new_order.product_offered_id)
        if not product_item:
            logger.info("El producto solicitado no está en base de datos")
            return ServiceResult(ProductOfferedExceptions.ProductOfferedNotFoundException())
        else:        
            product_price = product_item.product.price.price
            total = (product_price * new_order.quantity) - new_order.discount
        
        if (new_order.quantity <= 0):
            logger.info("La cantidad debe ser mayor a 0")
            return ServiceResult(OrderExceptions.OrderQuantityException())
        
        if (product_item and (new_order.quantity > product_item.quantity)):
            backlog = BacklogToSave(
                product_id=product_item.product_id,
                required_quantity=new_order.quantity - product_item.quantity,
                created_by=current_user.id,
                updated_by=uuid.UUID(int=0)
            )
            create_backlog = await BacklogRepository(self.db).create_backlog(backlog)
            if not create_backlog:
                logger.error("Error creating backlog")
                return ServiceResult(BacklogExceptions.BacklogCreateException())
            
            logger.info("La cantidad solicitada no está disponible")
            return ServiceResult(OrderExceptions.OrderQuantityNotAvailableException(product_item.quantity, new_order.quantity))
        
        if (product_price * new_order.quantity < new_order.discount):
            logger.info("El descuento no puede ser mayor al total")
            return ServiceResult(OrderExceptions.OrderDiscountException(product_price * new_order.quantity, new_order.discount))        
        else:
            new_order.total = total
            logger.info(f"Product price: {total}")

        order_item = await OrderRepository(self.db).create_order(new_order)

        if not order_item:
            logger.error("Error creating order")
            return ServiceResult(OrderExceptions.OrderCreateException())

        return ServiceResult(order_item)
    
    async def get_order_list(
        self,
        search: str | None,
        page_num: int = 1,
        page_size: int = 10,
        order: str = None,
        direction: str = None,
    ) -> ServiceResult:
        orders = await OrderRepository(self.db).get_order_list(search, order, direction)

        service_result = None
        if len(orders) == 0:
            service_result = ServiceResult([])
            service_result.status_code = 204
        else:
            response = short_pagination(
                page_num=page_num,
                page_size=page_size,
                data_list=orders,
                route=f"{API_PREFIX}/orders",
            )
            service_result = ServiceResult(response)

        return service_result
    
    async def get_order_by_id(self, id: UUID) -> ServiceResult:
        order_in_db = await OrderRepository(self.db).get_order_by_id(id=id)

        if isinstance(order_in_db, dict) and not order_in_db.get("id"):
            logger.info("El pedido solicitado no está en base de datos")
            return ServiceResult(OrderExceptions.OrderNotFoundException())

        order = OrderInDB(**order_in_db.dict())
        return ServiceResult(order)
    
    async def update_order(
        self, id: UUID, order_update: OrderUpdate, current_user: UserInDB
    ) -> ServiceResult:
        if not is_valid_uuid(id):
            return ServiceResult(OrderExceptions.OrderIdNoValidException())

        product_item = await ProductOfferedRepository(self.db).get_product_offered_by_id(id=order_update.product_offered_id)
        
        if not product_item:
            logger.info("El producto solicitado no está en base de datos")
            return ServiceResult(ProductOfferedExceptions.ProductOfferedNotFoundException())
        else:
            product_price = product_item.product.price.price
        
        if (order_update.quantity <= 0):
            logger.info("La cantidad debe ser mayor a 0")
            return ServiceResult(OrderExceptions.OrderQuantityException())
        
        if (product_item and (order_update.quantity > product_item.quantity)):
            logger.info("La cantidad solicitada no está disponible")
            return ServiceResult(OrderExceptions.OrderQuantityNotAvailableException(product_item.quantity, order_update.quantity))
       
        if (product_price * order_update.quantity < order_update.discount):
            logger.info("El descuento no puede ser mayor al total")
            return ServiceResult(OrderExceptions.OrderDiscountException(product_price * order_update.quantity, order_update.discount))      
        
        try:
            order = await OrderRepository(self.db).update_order(
                id=id,
                order_update=order_update,
                updated_by_id=current_user.id,
            )

            if isinstance(order, dict) and not order.get("id"):
                logger.info("El ID del pedido a actualizar no está en base de datos")
                return ServiceResult(OrderExceptions.OrderNotFoundException())

            return ServiceResult(OrderInDB(**order.dict()))

        except Exception as e:
            logger.error(f"Error: {e}")
            return ServiceResult(OrderExceptions.OrderInvalidUpdateParamsException(e))
    
    async def delete_order_by_id(
        self, id: UUID
    ) -> ServiceResult:
        
        order_id = await OrderRepository(self.db).delete_order_by_id(id=id)

        if isinstance(order_id, dict) and not order_id.get("id"):
            logger.info("El ID del pedido a eliminar no está en base de datos")
            return ServiceResult(OrderExceptions.OrderNotFoundException())
        
        return ServiceResult(order_id)
