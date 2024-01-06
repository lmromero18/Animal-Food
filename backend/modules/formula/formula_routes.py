from typing import Dict, List, Optional, Union
from uuid import UUID
from databases import Database
from fastapi import APIRouter, Body, Depends, Path, status
from loguru import logger

from modules.formula.formula_schemas import (
    FormulaCreate,
    FormulaInDB,
    FormulaUpdate
)

from modules.users.users.user_schemas import (
    UserInDB
)

from modules.users.auths.auth_dependencies import get_current_active_user
from modules.users.auths.auth_exceptions import AuthExceptions
from shared.core.db.db_dependencies import get_database
from shared.utils.service_result import ServiceResult, handle_result
from shared.utils.verify_auth import is_authorized
from modules.formula.formula_services import FormulaService

formula_router = APIRouter(
    prefix="/formula",
    tags=["formula"],
    responses={404: {"description": "Not found"}},
)

@formula_router.post(
    "/",
    response_model=FormulaInDB,
    status_code=status.HTTP_201_CREATED,
    name="formula:create-formula",
)
async def create_formula(
    formula: Optional[FormulaCreate] = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "formula:create-formula"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    
    result = await FormulaService(db).create_formula(formula, current_user)
    return handle_result(result)

@formula_router.get(
    "/",  
    name="formula:formula-list", 
    status_code=status.HTTP_200_OK
)
async def get_formula_list(
    search: str | None = None,
    page_number: int = 1,
    page_size: int = 10,
    order: str = "",
    direction: str = "",
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "formula:get-formula-list"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await FormulaService(db).get_formula_list(
        search,
        page_num=page_number,
        page_size=page_size,
        order=order,
        direction=direction,
    )
    return handle_result(result)

@formula_router.get(
    "/{id}", 
    response_model=Dict, 
    name="formula:get-formula-by-id")
async def get_formula_by_id(
    id: UUID = Path(..., title="The id of the formula to get"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "formula:get-formula-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await FormulaService(db).get_formula_by_id(id=id)
    return handle_result(result)

@formula_router.put(
    "/{id}", 
    response_model=Dict, 
    name="formula:update-formula-by-id"
)
async def update_formula_by_id(
    id: UUID = Path(..., title="The id of the formula to update"),
    formula_update: FormulaUpdate = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "formula:update-formula-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await FormulaService(db).update_formula(
        id=id, formula_update=formula_update, current_user=current_user
    )
    return handle_result(result)

@formula_router.delete(
    "/{id}", 
    response_model=Dict, 
    name="formula:delete-formula-by-id"
)
async def delete_formula_by_id(
    id: UUID = Path(..., title="The id of the formula to delete"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "formula:delete-formula-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await FormulaService(db).delete_formula_by_id(
        id=id
    )
    return handle_result(result)