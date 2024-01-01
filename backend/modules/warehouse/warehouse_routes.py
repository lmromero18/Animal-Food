from typing import Dict, List, Optional, Union
from databases import Database
from fastapi import APIRouter, Body, Depends, Path, status
from loguru import logger

from modules.warehouse.warehouse_schemas import (
    WarehouseCreateSchema,
    WarehouseToSaveSchema,
    #PENDIENTE
)

from modules.users.users.user_schemas import (
    UserInDB
)

from users.auths.auth_dependencies import get_current_active_user
from users.auths.auth_exceptions import AuthExceptions
from shared.core.db.db_dependencies import get_database
from shared.utils.service_result import ServiceResult, handle_result
from shared.utils.verify_auth import is_authorized

warehouse_router = APIRouter(
    prefix="/warehouse",
    tags=["warehouse"],
    responses={404: {"description": "Not found"}},
)
