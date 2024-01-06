from modules.raw_material.raw_material_repositories import RawMaterialRepository
from modules.product.product_repositories import ProductRepository
from modules.warehouse.warehouse_repositories import WarehouseRepository
from databases import Database
from loguru import logger
from typing import List
from uuid import UUID

from modules.formula.formula_exceptions import FormulaExceptions
from modules.formula.formula_schemas import (
    FormulaCreate,
    FormulaInDB,
    FormulaToSave,
    FormulaUpdate
)

from shared.utils.record_to_dict import record_to_dict
import shared.utils.repository_utils as ru

class FormulaRepository:
    def __init__(self, db: Database):
        self.db = db
        
    async def get_complete_formula(self, record):
        formula = FormulaInDB(**dict(record))
        if (formula.raw_material_id):            
            raw_material = await RawMaterialRepository(self.db).get_raw_material_by_id(formula.raw_material_id)
            if raw_material:
                formula.raw_material = raw_material
            else:
                raise FormulaExceptions.FormulaInvalidWarehouseIdException()
            
        if (formula.product_id):            
            product = await ProductRepository(self.db).get_product_by_id(formula.product_id)
            if product:
                formula.product = product
            else:
                raise FormulaExceptions.FormulaInvalidProductIdException()
        return formula
    
    async def create_formula(self, formula: FormulaToSave) -> FormulaInDB:
        from modules.formula.formula_sqlstatements import CREATE_FORMULA_ITEM

        values = ru.preprocess_create(formula.dict())
        record = await self.db.fetch_one(query=CREATE_FORMULA_ITEM, values=values)

        return await self.get_complete_formula(record_to_dict(record))

    
    async def get_formula_list(
        self,
        search: str | None,
        order: str | None,
        direction: str | None,
    ) -> List:
        from modules.formula.formula_sqlstatements import (
            GET_FORMULA_LIST,
            formula_list_complements,
            formula_list_search,
        )

        order = order.lower() if order != None else None
        direction = direction.upper() if order != None else None
        values = {}
        sql_sentence = formula_list_complements(order, direction)
        sql_search = formula_list_search()

        if not search:
            sql_sentence = GET_FORMULA_LIST + sql_sentence
        else:
            sql_sentence = GET_FORMULA_LIST + sql_search + sql_sentence
            values["search"] = "%" + search + "%"

        records = await self.db.fetch_all(query=sql_sentence, values=values)

        if len(records) == 0 or not records:
            return []
        
        return [await self.get_complete_formula(record) for record in records]
    
    async def get_formula_by_id(self, id: UUID) -> FormulaInDB | dict:
        from modules.formula.formula_sqlstatements import GET_FORMULA_BY_ID

        values = {"id": id}
        record = await self.db.fetch_one(query=GET_FORMULA_BY_ID, values=values)
        if not record:
            return {}

        return await self.get_complete_formula(record_to_dict(record))

    
    async def update_formula(
        self,
        id: UUID,
        formula_update: FormulaUpdate,
        updated_by_id: UUID,
    ) -> FormulaInDB | dict:
        from modules.formula.formula_sqlstatements import UPDATE_FORMULA_BY_ID

        formula = await self.get_formula_by_id(id=id)
        if not formula:
            return {}

        formula_update_params = formula.copy(update=formula_update.dict(exclude_unset=True))
            
        formula_params_dict = dict(formula_update_params)
        formula_params_dict["updated_by"] = updated_by_id
        formula_params_dict["updated_at"] = ru._preprocess_date()        
        
        # If warehouse is present, remove it from the dictionary so that it is not updated
        if "raw_material" in formula_params_dict:
            del formula_params_dict["raw_material"]
        
        # If product is present, remove it from the dictionary so that it is not updated  
        if "product" in formula_params_dict:
            del formula_params_dict["product"]
        
        try:
            record = await self.db.fetch_one(query=UPDATE_FORMULA_BY_ID, values=formula_params_dict)
            formula_updated = record_to_dict(record)
            return await self.get_formula_by_id(id=formula_updated.get("id"))
        except Exception as e:
            logger.error(f"Invalid data to update a formula: {e}")
            raise FormulaExceptions.FormulaInvalidUpdateParamsException()
        
    async def delete_formula_by_id(
        self,
        id: UUID,
    ) -> UUID | dict:
        from modules.formula.formula_sqlstatements import DELETE_FORMULA_BY_ID

        formula = await self.get_formula_by_id(id=id)

        if not formula:
            return {}
        
        record = await self.db.fetch_one(query=DELETE_FORMULA_BY_ID, values={"id": id})
        formula_id_delete = dict(record)        

        return formula_id_delete