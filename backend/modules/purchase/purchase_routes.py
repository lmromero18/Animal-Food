from typing import Dict, List, Optional, Union
from uuid import UUID
from databases import Database
from fastapi import APIRouter, Body, Depends, Path, status
from loguru import logger

from modules.purchase.purchase_schemas import (
    PurchaseCreate,
    PurchaseInDB,
    PurchaseUpdate
)

from modules.users.users.user_schemas import (
    UserInDB
)

from modules.users.auths.auth_dependencies import get_current_active_user
from modules.users.auths.auth_exceptions import AuthExceptions
from shared.core.db.db_dependencies import get_database
from shared.utils.service_result import ServiceResult, handle_result
from shared.utils.verify_auth import is_authorized
from modules.purchase.purchase_services import PurchaseService

purchase_router = APIRouter(
    prefix="/purchase",
    tags=["purchase"],
    responses={404: {"description": "Not found"}},
)

@purchase_router.post(
    "/",
    response_model=PurchaseInDB,
    status_code=status.HTTP_201_CREATED,
    name="purchase:create-purchase",
)
async def create_purchase(
    purchase: Optional[PurchaseCreate] = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "purchase:create-purchase"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    
    result = await PurchaseService(db).create_purchase(purchase, current_user)
    return handle_result(result)

@purchase_router.get(
    "/",  
    name="purchase:purchase_list", 
    status_code=status.HTTP_200_OK
)
async def get_purchase_list(
    search: str | None = None,
    page_number: int = 1,
    page_size: int = 10,
    order: str = "",
    direction: str = "",
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "purchase:get_purchase_list"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await PurchaseService(db).get_purchase_list(
        search,
        page_num=page_number,
        page_size=page_size,
        order=order,
        direction=direction,
    )
    return handle_result(result)

@purchase_router.get(
    "/{id}", 
    response_model=Dict, 
    name="purchase:get-purchase-by-id")
async def get_purchase_by_id(
    id: UUID = Path(..., title="The id of the purchase to get"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "purchase:get-purchase-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await PurchaseService(db).get_purchase_by_id(id=id)
    return handle_result(result)

@purchase_router.put(
    "/{id}", 
    response_model=Dict, 
    name="purchase:update-purchase-by-id"
)
async def update_purchase_by_id(
    id: UUID = Path(..., title="The id of the purchase to update"),
    purchase_update: PurchaseUpdate = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "purchase:update-purchase-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await PurchaseService(db).update_purchase(
        id=id, purchase_update=purchase_update, current_user=current_user
    )
    return handle_result(result)

@purchase_router.delete(
    "/{id}", 
    response_model=Dict, 
    name="purchase:delete-purchase-by-id"
)
async def delete_purchase_by_id(
    id: UUID = Path(..., title="The id of the purchase to update"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "purchase:delete-purchase-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await PurchaseService(db).delete_purchase_by_id(
        id=id
    )
    return handle_result(result)
