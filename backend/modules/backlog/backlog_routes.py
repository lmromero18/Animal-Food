from typing import Dict, List, Optional, Union
from uuid import UUID
from databases import Database
from fastapi import APIRouter, Body, Depends, Path, status
from loguru import logger

from modules.backlog.backlog_schemas import (
    BacklogCreate,
    BacklogInDB,
    BacklogUpdate
)

from modules.users.users.user_schemas import (
    UserInDB
)

from modules.users.auths.auth_dependencies import get_current_active_user
from modules.users.auths.auth_exceptions import AuthExceptions
from shared.core.db.db_dependencies import get_database
from shared.utils.service_result import ServiceResult, handle_result
from shared.utils.verify_auth import is_authorized
from modules.backlog.backlog_services import BacklogService

backlog_router = APIRouter(
    prefix="/backlog",
    tags=["backlog"],
    responses={404: {"description": "Not found"}},
)

@backlog_router.post(
    "/",
    response_model=BacklogInDB,
    status_code=status.HTTP_201_CREATED,
    name="backlog:create-backlog",
)
async def create_backlog(
    backlog: Optional[BacklogCreate] = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "backlog:create-backlog"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    
    result = await BacklogService(db).create_backlog(backlog, current_user)
    return handle_result(result)

@backlog_router.get(
    "/",  
    name="backlog:backlog_list", 
    status_code=status.HTTP_200_OK
)
async def get_backlog_list(
    search: str | None = None,
    page_number: int = 1,
    page_size: int = 10,
    order: str = "",
    direction: str = "",
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "backlog:get_backlog_list"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await BacklogService(db).get_backlog_list(
        search,
        page_num=page_number,
        page_size=page_size,
        order=order,
        direction=direction,
    )
    return handle_result(result)

@backlog_router.get(
    "/{id}", 
    response_model=Dict, 
    name="backlog:get-backlog-by-id")
async def get_backlog_by_id(
    id: UUID = Path(..., title="The id of the backlog to get"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "users:get-backlog-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await BacklogService(db).get_backlog_by_id(id=id)
    return handle_result(result)

@backlog_router.put(
    "/{id}", 
    response_model=Dict, 
    name="backlog:update-backlog-by-id"
)
async def update_backlog_by_id(
    id: UUID = Path(..., title="The id of the backlog to update"),
    backlog_update: BacklogUpdate = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "backlog:update-backlog-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await BacklogService(db).update_backlog(
        id=id, backlog_update=backlog_update, current_user=current_user
    )
    return handle_result(result)

@backlog_router.delete(
    "/{id}", 
    response_model=Dict, 
    name="backlog:delete-backlog-by-id"
)
async def delete_backlog_by_id(
    id: UUID = Path(..., title="The id of the backlog to update"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "backlog:delete-backlog-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await BacklogService(db).delete_backlog_by_id(id=id)
    return handle_result(result)
