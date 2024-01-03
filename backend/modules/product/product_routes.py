from typing import Dict, List, Optional, Union
from uuid import UUID
from databases import Database
from fastapi import APIRouter, Body, Depends, Path, status
from loguru import logger

from modules.product.product_schemas import (
    ProductCreate,
    ProductInDB,
    ProductUpdate
)

from modules.users.users.user_schemas import (
    UserInDB
)

from modules.users.auths.auth_dependencies import get_current_active_user
from modules.users.auths.auth_exceptions import AuthExceptions
from shared.core.db.db_dependencies import get_database
from shared.utils.service_result import ServiceResult, handle_result
from shared.utils.verify_auth import is_authorized
from modules.product.product_services import ProductService

product_router = APIRouter(
    prefix="/product",
    tags=["product"],
    responses={404: {"description": "Not found"}},
)

@product_router.post(
    "/",
    response_model=ProductInDB,
    status_code=status.HTTP_201_CREATED,
    name="product:create-product",
)
async def create_product(
    product: Optional[ProductCreate] = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "product:create-product"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    
    result = await ProductService(db).create_product(product, current_user)
    return handle_result(result)

@product_router.get(
    "/",  
    name="product:product_list", 
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
    if not is_authorized(current_user, "product:get_product_list"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await ProductService(db).get_product_list(
        search,
        page_num=page_number,
        page_size=page_size,
        order=order,
        direction=direction,
    )
    return handle_result(result)

@product_router.get(
    "/{id}", 
    response_model=Dict, 
    name="product:get-product-by-id")
async def get_product_by_id(
    id: UUID = Path(..., title="The id of the product to get"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "users:get-product-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await ProductService(db).get_product_by_id(id=id)
    return handle_result(result)

@product_router.put(
    "/{id}", 
    response_model=Dict, 
    name="product:update-product-by-id"
)
async def update_product_by_id(
    id: UUID = Path(..., title="The id of the product to update"),
    product_update: ProductUpdate = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "product:update-product-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await ProductService(db).update_product(
        id=id, product_update=product_update, current_user=current_user
    )
    return handle_result(result)

@product_router.delete(
    "/{id}", 
    response_model=Dict, 
    name="product:delete-product-by-id"
)
async def delete_product_by_id(
    id: UUID = Path(..., title="The id of the product to update"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "product:delete-product-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await ProductService(db).delete_product_by_id(
        id=id
    )
    return handle_result(result)