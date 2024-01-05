from typing import Dict, List, Optional, Union
from uuid import UUID
from databases import Database
from fastapi import APIRouter, Body, Depends, Path, status
from loguru import logger

from modules.product_offered.product_offered_schemas import (
    ProductOfferedCreate,
    ProductOfferedInDB,
    ProductOfferedUpdate
)

from modules.users.users.user_schemas import (
    UserInDB
)

from modules.users.auths.auth_dependencies import get_current_active_user
from modules.users.auths.auth_exceptions import AuthExceptions
from shared.core.db.db_dependencies import get_database
from shared.utils.service_result import ServiceResult, handle_result
from shared.utils.verify_auth import is_authorized
from modules.product_offered.product_offered_services import ProductOfferedService

product_offered_router = APIRouter(
    prefix="/product-offered",
    tags=["product-offered"],
    responses={404: {"description": "Not found"}},
)

@product_offered_router.post(
    "/",
    response_model=ProductOfferedInDB,
    status_code=status.HTTP_201_CREATED,
    name="product-offered:create-product-offered",
)
async def create_product(
    product: Optional[ProductOfferedCreate] = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "product-offered:create-product-offered"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    
    result = await ProductOfferedService(db).create_product_offered(product, current_user)
    return handle_result(result)

@product_offered_router.get(
    "/",  
    name="product-offered:product-offered-list", 
    status_code=status.HTTP_200_OK
)
async def get_product_list(
    search: str | None = None,
    page_number: int = 1,
    page_size: int = 10,
    order: str = "",
    direction: str = "",
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "product-offered:get-product-list"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await ProductOfferedService(db).get_product_offered_list(
        search,
        page_num=page_number,
        page_size=page_size,
        order=order,
        direction=direction,
    )
    return handle_result(result)

@product_offered_router.get(
    "/{id}", 
    response_model=Dict, 
    name="product-offered:get-product-offered-by-id")
async def get_product_by_id(
    id: UUID = Path(..., title="The id of the product offered to get"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "users:get-product-offered-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await ProductOfferedService(db).get_product_offered_by_id(id=id)
    return handle_result(result)

@product_offered_router.put(
    "/{id}", 
    response_model=Dict, 
    name="product-offered:update-product-offered-by-id"
)
async def update_product_offered_by_id(
    id: UUID = Path(..., title="The id of the product to update"),
    product_offered_update: ProductOfferedUpdate = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "product-offered:update-product-offered-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await ProductOfferedService(db).update_product_offered(
        id=id, product_offered_update=product_offered_update, current_user=current_user
    )
    return handle_result(result)

@product_offered_router.delete(
    "/{id}", 
    response_model=Dict, 
    name="product-offered:delete-product-offered-by-id"
)
async def delete_product_by_id(
    id: UUID = Path(..., title="The id of the product offered to update"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "product:delete-product-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await ProductOfferedService(db).delete_product_offered_by_id(
        id=id
    )
    return handle_result(result)