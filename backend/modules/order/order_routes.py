from typing import Dict, List, Optional, Union
from uuid import UUID
from databases import Database
from fastapi import APIRouter, Body, Depends, Path, status
from loguru import logger

from modules.order.order_schemas import (
    OrderCreate,
    OrderInDB,
    OrderUpdate
)

from modules.users.users.user_schemas import (
    UserInDB
)

from modules.users.auths.auth_dependencies import get_current_active_user
from modules.users.auths.auth_exceptions import AuthExceptions
from shared.core.db.db_dependencies import get_database
from shared.utils.service_result import ServiceResult, handle_result
from shared.utils.verify_auth import is_authorized
from modules.order.order_services import OrderService

order_router = APIRouter(
    prefix="/order",
    tags=["order"],
    responses={404: {"description": "Not found"}},
)

@order_router.post(
    "/",
    response_model=OrderInDB,
    status_code=status.HTTP_201_CREATED,
    name="order:create-order",
)
async def create_order(
    order: Optional[OrderCreate] = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "order:create-order"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    
    result = await OrderService(db).create_order(order, current_user)
    return handle_result(result)

@order_router.get(
    "/",  
    name="order:order_list", 
    status_code=status.HTTP_200_OK
)
async def get_order_list(
    search: str | None = None,
    page_number: int = 1,
    page_size: int = 10,
    order: str = "",
    direction: str = "",
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "order:get_order_list"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await OrderService(db).get_order_list(
        search,
        page_num=page_number,
        page_size=page_size,
        order=order,
        direction=direction,
    )
    return handle_result(result)

@order_router.get(
    "/{id}", 
    response_model=Dict, 
    name="order:get-order-by-id")
async def get_order_by_id(
    id: UUID = Path(..., title="The id of the order to get"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "order:get-order-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await OrderService(db).get_order_by_id(id=id)
    return handle_result(result)

@order_router.put(
    "/{id}", 
    response_model=Dict, 
    name="order:update-order-by-id"
)
async def update_order_by_id(
    id: UUID = Path(..., title="The id of the order to update"),
    order_update: OrderUpdate = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "order:update-order-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await OrderService(db).update_order(
        id=id, order_update=order_update, current_user=current_user
    )
    return handle_result(result)

@order_router.delete(
    "/{id}", 
    response_model=Dict, 
    name="order:delete-order-by-id"
)
async def delete_order_by_id(
    id: UUID = Path(..., title="The id of the order to update"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "order:delete-order-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await OrderService(db).delete_order_by_id(
        id=id
    )
    return handle_result(result)
