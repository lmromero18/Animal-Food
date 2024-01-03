from typing import Dict, List, Optional, Union
from uuid import UUID
from databases import Database
from fastapi import APIRouter, Body, Depends, Path, status
from loguru import logger

from modules.warehouse.warehouse_schemas import (
    WarehouseCreate,
    WarehouseInDB,
    WarehouseUpdate
)

from modules.users.users.user_schemas import (
    UserInDB
)

from modules.users.auths.auth_dependencies import get_current_active_user
from modules.users.auths.auth_exceptions import AuthExceptions
from shared.core.db.db_dependencies import get_database
from shared.utils.service_result import ServiceResult, handle_result
from shared.utils.verify_auth import is_authorized
from modules.warehouse.warehouse_services import WarehouseService

warehouse_router = APIRouter(
    prefix="/warehouse",
    tags=["warehouse"],
    responses={404: {"description": "Not found"}},
)

@warehouse_router.post(
    "/",
    response_model=WarehouseInDB,
    status_code=status.HTTP_201_CREATED,
    name="warehouse:create-warehouse",
)
async def create_warehouse(
    warehouse: Optional[WarehouseCreate] = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "warehouse:create-warehouse"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    
    result = await WarehouseService(db).create_warehouse(warehouse, current_user)
    return handle_result(result)

@warehouse_router.get(
    "/",  
    name="warehouse:warehouse_list", 
    status_code=status.HTTP_200_OK
)
async def get_warehouse_list(
    search: str | None = None,
    page_number: int = 1,
    page_size: int = 10,
    order: str = "",
    direction: str = "",
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "warehouse:get_warehouse_list"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await WarehouseService(db).get_warehouse_list(
        search,
        page_num=page_number,
        page_size=page_size,
        order=order,
        direction=direction,
    )
    return handle_result(result)

@warehouse_router.get(
    "/{id}", 
    response_model=Dict, 
    name="warehouse:get-warehouse-by-id")
async def get_warehouse_by_id(
    id: UUID = Path(..., title="The id of the warehouse to get"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "users:get-warehouse-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await WarehouseService(db).get_warehouse_by_id(id=id)
    return handle_result(result)

@warehouse_router.put(
    "/{id}", 
    response_model=Dict, 
    name="warehouse:update-warehouse-by-id"
)
async def update_warehouse_by_id(
    id: UUID = Path(..., title="The id of the warehouse to update"),
    warehouse_update: WarehouseUpdate = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "warehouse:update-warehouse-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await WarehouseService(db).update_warehouse(
        id=id, warehouse_update=warehouse_update, current_user=current_user
    )
    return handle_result(result)

@warehouse_router.delete(
    "/{id}", 
    response_model=Dict, 
    name="warehouse:delete-warehouse-by-id"
)
async def delete_warehouse_by_id(
    id: UUID = Path(..., title="The id of the warehouse to update"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "warehouse:delete-warehouse-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await WarehouseService(db).delete_warehouse_by_id(
        id=id
    )
    return handle_result(result)