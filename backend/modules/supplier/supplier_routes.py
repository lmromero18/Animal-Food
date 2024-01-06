from typing import Dict, List, Optional, Union
from uuid import UUID
from databases import Database
from fastapi import APIRouter, Body, Depends, Path, status
from loguru import logger

from modules.supplier.supplier_schemas import (
    SupplierCreate,
    SupplierInDB,
    SupplierUpdate
)

from modules.users.users.user_schemas import (
    UserInDB
)

from modules.users.auths.auth_dependencies import get_current_active_user
from modules.users.auths.auth_exceptions import AuthExceptions
from shared.core.db.db_dependencies import get_database
from shared.utils.service_result import ServiceResult, handle_result
from shared.utils.verify_auth import is_authorized
from modules.supplier.supplier_services import SupplierService

supplier_router = APIRouter(
    prefix="/supplier",
    tags=["supplier"],
    responses={404: {"description": "Not found"}},
)

@supplier_router.post(
    "/",
    response_model=SupplierInDB,
    status_code=status.HTTP_201_CREATED,
    name="supplier:create-supplier",
)
async def create_supplier(
    supplier: Optional[SupplierCreate] = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "supplier:create-supplier"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    
    result = await SupplierService(db).create_supplier(supplier, current_user)
    return handle_result(result)

@supplier_router.get(
    "/",  
    name="supplier:supplier_list", 
    status_code=status.HTTP_200_OK
)
async def get_supplier_list(
    search: str | None = None,
    page_number: int = 1,
    page_size: int = 10,
    order: str = "",
    direction: str = "",
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "supplier:get_supplier_list"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await SupplierService(db).get_supplier_list(
        search,
        page_num=page_number,
        page_size=page_size,
        order=order,
        direction=direction,
    )
    return handle_result(result)

@supplier_router.get(
    "/{id}", 
    response_model=Dict, 
    name="supplier:get-supplier-by-id")
async def get_supplier_by_id(
    id: UUID = Path(..., title="The id of the supplier to get"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "supplier:get-supplier-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await SupplierService(db).get_supplier_by_id(id=id)
    return handle_result(result)

@supplier_router.put(
    "/{id}", 
    response_model=Dict, 
    name="supplier:update-supplier-by-id"
)
async def update_supplier_by_id(
    id: UUID = Path(..., title="The id of the supplier to update"),
    supplier_update: SupplierUpdate = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "supplier:update-supplier-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await SupplierService(db).update_supplier(
        id=id, supplier_update=supplier_update, current_user=current_user
    )
    return handle_result(result)

@supplier_router.delete(
    "/{id}", 
    response_model=Dict, 
    name="supplier:delete-supplier-by-id"
)
async def delete_supplier_by_id(
    id: UUID = Path(..., title="The id of the supplier to update"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "supplier:delete-supplier-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await SupplierService(db).delete_supplier_by_id(
        id=id
    )
    return handle_result(result)
