from typing import Dict, List, Optional, Union
from uuid import UUID
from databases import Database
from fastapi import APIRouter, Body, Depends, Path, status
from loguru import logger

from modules.raw_material.raw_material_schemas import (
    RawMaterialCreate,
    RawMaterialInDB,
    RawMaterialUpdate
)

from modules.users.users.user_schemas import (
    UserInDB
)

from modules.users.auths.auth_dependencies import get_current_active_user
from modules.users.auths.auth_exceptions import AuthExceptions
from shared.core.db.db_dependencies import get_database
from shared.utils.service_result import ServiceResult, handle_result
from shared.utils.verify_auth import is_authorized
from modules.raw_material.raw_material_services import RawMaterialService

raw_material_router = APIRouter(
    prefix="/raw_material",
    tags=["raw_material"],
    responses={404: {"description": "Not found"}},
)

@raw_material_router.post(
    "/",
    response_model=RawMaterialInDB,
    status_code=status.HTTP_201_CREATED,
    name="raw_material:create-raw-material",
)
async def create_raw_material(
    raw_material: Optional[RawMaterialCreate] = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "raw_material:create-raw-material"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    
    result = await RawMaterialService(db).create_raw_material(raw_material, current_user)
    return handle_result(result)

@raw_material_router.get(
    "/",  
    name="raw_material:raw_material_list", 
    status_code=status.HTTP_200_OK
)
async def get_raw_material_list(
    search: str | None = None,
    page_number: int = 1,
    page_size: int = 10,
    order: str = "",
    direction: str = "",
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "raw_material:get_raw_material_list"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await RawMaterialService(db).get_raw_material_list(
        search,
        page_num=page_number,
        page_size=page_size,
        order=order,
        direction=direction,
    )
    return handle_result(result)

@raw_material_router.get(
    "/{id}", 
    response_model=Dict, 
    name="raw_material:get-raw-material-by-id")
async def get_raw_material_by_id(
    id: UUID = Path(..., title="The id of the raw material to get"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "raw_material:get-raw-material-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await RawMaterialService(db).get_raw_material_by_id(id=id)
    return handle_result(result)

@raw_material_router.put(
    "/{id}", 
    response_model=Dict, 
    name="raw_material:update-raw-material-by-id"
)
async def update_raw_material_by_id(
    id: UUID = Path(..., title="The id of the raw material to update"),
    raw_material_update: RawMaterialUpdate = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "raw_material:update-raw-material-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await RawMaterialService(db).update_raw_material(
        id=id, raw_material_update=raw_material_update, current_user=current_user
    )
    return handle_result(result)

@raw_material_router.delete(
    "/{id}", 
    response_model=Dict, 
    name="raw_material:delete-raw-material-by-id"
)
async def delete_raw_material_by_id(
    id: UUID = Path(..., title="The id of the raw material to update"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "raw_material:delete-raw-material-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await RawMaterialService(db).delete_raw_material_by_id(
        id=id
    )
    return handle_result(result)