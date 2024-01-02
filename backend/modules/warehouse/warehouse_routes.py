from typing import Dict, List, Optional, Union
from databases import Database
from fastapi import APIRouter, Body, Depends, Path, status
from loguru import logger

from modules.warehouse.warehouse_schemas import (
    WarehouseCreate,
    WarehouseInDB,
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
