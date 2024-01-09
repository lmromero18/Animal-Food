from typing import List
from uuid import UUID
import uuid
from modules.raw_material.raw_material_exceptions import RawMaterialExceptions
from modules.raw_material.raw_material_repositories import RawMaterialRepository
from modules.product.product_exceptions import ProductExceptions
from modules.product.product_repositories import ProductRepository
from modules.warehouse.warehouse_exceptions import WarehouseExceptions
from modules.warehouse.warehouse_services import WarehouseService
from shared.utils.record_to_dict import record_to_dict
from shared.utils.verify_uuid import is_valid_uuid

from databases import Database
import fastapi
from loguru import logger

from shared.utils.service_result import ServiceResult
from modules.formula.formula_repositories import FormulaRepository
from modules.formula.formula_exceptions import FormulaExceptions
from modules.formula.formula_schemas import (
    FormulaCreate,
    FormulaToSave,
    FormulaInDB,
    FormulaUpdate
)
from modules.users.users.user_schemas import UserInDB
from shared.core.config import API_PREFIX
import shared.utils.repository_utils as ru
from shared.utils.short_pagination import short_pagination

class FormulaService:
    def __init__(self, db: Database):
        self.db = db
  
    async def create_formula(
        self, formula: FormulaCreate, current_user: UserInDB):

        new_formula = FormulaToSave(**formula.dict())
        new_formula.created_by = current_user.id
        new_formula.updated_by = uuid.UUID(int=0)
        
        product_id_exists = await ProductRepository(self.db).get_product_by_id(id=new_formula.product_id)
        if not product_id_exists:
            logger.info("The product does not exist in the database")
            return ServiceResult(ProductExceptions.ProductNotFoundException())
        
        if new_formula.required_quantity <= 0:
            logger.info("The quantity must be greater than 0")
            return ServiceResult(FormulaExceptions.LowQuantityException())
        
        raw_material_id_exists = await RawMaterialRepository(self.db).get_raw_material_by_id(id=new_formula.raw_material_id)
        if not raw_material_id_exists:
            logger.info("The raw material does not exist in the database")
            return ServiceResult(RawMaterialExceptions.RawMaterialNotFoundException())

        formula_item = await FormulaRepository(self.db).create_formula(new_formula)

        if not formula_item:
            logger.error("Error creating formula")
            return ServiceResult(FormulaExceptions.FormulaCreateException())

        return ServiceResult(formula_item)
    
    async def get_formula_list(
        self,
        search: str | None,
        page_num: int = 1,
        page_size: int = 10,
        order: str = None,
        direction: str = None,
    ) -> ServiceResult:
        formula_list = await FormulaRepository(self.db).get_formula_list(search, order, direction)

        service_result = None
        if len(formula_list) == 0:
            service_result = ServiceResult([])
            service_result.status_code = 204
        else:
            response = short_pagination(
                page_num=page_num,
                page_size=page_size,
                data_list=formula_list,
                route=f"{API_PREFIX}/formula",
            )
            service_result = ServiceResult(response)

        return service_result
    
    async def get_formula_by_id(self, id: UUID) -> ServiceResult:
        formula_in_db = await FormulaRepository(self.db).get_formula_by_id(id=id)

        if isinstance(formula_in_db, dict) and not formula_in_db.get("id"):
            logger.info("The requested formula is not in the database")
            return ServiceResult(FormulaExceptions.FormulaNotFoundException())

        formula = FormulaInDB(**formula_in_db.dict())
        return ServiceResult(formula)
    
    async def update_formula(
        self, id: UUID, formula_update: FormulaUpdate, current_user: UserInDB
    ) -> ServiceResult:
        if not is_valid_uuid(id):
            return ServiceResult(FormulaExceptions.FormulaIdNoValidException())
        
        if formula_update.required_quantity <= 0:
            logger.info("The quantity must be greater than 0")
            return ServiceResult(FormulaExceptions.LowQuantityException())
        
        product_id_exists = await ProductRepository(self.db).get_product_by_id(id=formula_update.product_id)
        if not product_id_exists:
            logger.info("The product does not exist in the database")
            return ServiceResult(ProductExceptions.ProductNotFoundException())
        
        raw_material_id_exists = await RawMaterialRepository(self.db).get_raw_material_by_id(id=formula_update.raw_material_id)
        if not raw_material_id_exists:
            logger.info("The raw material does not exist in the database")
            return ServiceResult(RawMaterialExceptions.RawMaterialNotFoundException())

        try:
            formula = await FormulaRepository(self.db).update_formula(
                id=id,
                formula_update=formula_update,
                updated_by_id=current_user.id,
            )
            
            logger.info(f"formula: {formula}")

            if isinstance(formula, dict) and not formula.get("id"):
                logger.info("The ID of the formula to update is not in the database")
                return ServiceResult(FormulaExceptions.FormulaNotFoundException())

            return ServiceResult(FormulaInDB(**formula.dict()))

        except Exception as e:
            logger.error(f"Error: {e}")
            return ServiceResult(FormulaExceptions.FormulaInvalidUpdateParamsException(e))
    
    async def delete_formula_by_id(
        self, id: UUID
    ) -> ServiceResult:
        
        formula_id = await FormulaRepository(self.db).delete_formula_by_id(id=id)

        if isinstance(formula_id, dict) and not formula_id.get("id"):
            logger.info("The ID of the formula to delete is not in the database")
            return ServiceResult(FormulaExceptions.FormulaNotFoundException())
        
        return ServiceResult(formula_id)