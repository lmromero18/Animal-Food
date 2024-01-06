from typing import Dict, List, Optional, Union
from uuid import UUID
from databases import Database
from fastapi import APIRouter, Body, Depends, Path, status
from loguru import logger

from modules.price.price_schemas import (
    PriceCreate,
    PriceInDB,
    PriceUpdate
)

from modules.users.users.user_schemas import (
    UserInDB
)

from modules.users.auths.auth_dependencies import get_current_active_user
from modules.users.auths.auth_exceptions import AuthExceptions
from shared.core.db.db_dependencies import get_database
from shared.utils.service_result import ServiceResult, handle_result
from shared.utils.verify_auth import is_authorized
from modules.price.price_services import PriceService

price_router = APIRouter(
    prefix="/price",
    tags=["price"],
    responses={404: {"description": "Not found"}},
)

@price_router.post(
    "/",
    response_model=PriceInDB,
    status_code=status.HTTP_201_CREATED,
    name="price:create-price",
)
async def create_price(
    price: Optional[PriceCreate] = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "price:create-price"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    
    result = await PriceService(db).create_price(price, current_user)
    return handle_result(result)

@price_router.get(
    "/",  
    name="price:price_list", 
    status_code=status.HTTP_200_OK
)
async def get_price_list(
    search: str | None = None,
    page_number: int = 1,
    page_size: int = 10,
    order: str = "",
    direction: str = "",
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "price:get_price_list"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await PriceService(db).get_price_list(
        search,
        page_num=page_number,
        page_size=page_size,
        order=order,
        direction=direction,
    )
    return handle_result(result)

@price_router.get(
    "/{id}", 
    response_model=Dict, 
    name="price:get-price-by-id")
async def get_price_by_id(
    id: UUID = Path(..., title="The id of the price to get"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "price:get-price-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await PriceService(db).get_price_by_id(id=id)
    return handle_result(result)

@price_router.put(
    "/{id}", 
    response_model=Dict, 
    name="price:update-price-by-id"
)
async def update_price_by_id(
    id: UUID = Path(..., title="The id of the price to update"),
    price_update: PriceUpdate = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "price:update-price-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await PriceService(db).update_price(
        id=id, price_update=price_update, current_user=current_user
    )
    return handle_result(result)

@price_router.delete(
    "/{id}", 
    response_model=Dict, 
    name="price:delete-price-by-id"
)
async def delete_price_by_id(
    id: UUID = Path(..., title="The id of the price to update"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "price:delete-price-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await PriceService(db).delete_price_by_id(
        id=id
    )
    return handle_result(result)