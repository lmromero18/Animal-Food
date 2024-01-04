from typing import List
from uuid import UUID
import uuid
from shared.utils.record_to_dict import record_to_dict
from shared.utils.verify_uuid import is_valid_uuid

from databases import Database
import fastapi
from loguru import logger

from shared.utils.service_result import ServiceResult
from modules.raw_material.raw_material_repositories import RawMaterialRepository
from modules.raw_material.raw_material_exceptions import RawMaterialExceptions
from modules.raw_material.raw_material_schemas import (
    RawMaterialCreate,
    RawMaterialToSave,
    RawMaterialInDB,
    RawMaterialUpdate
)
from modules.users.users.user_schemas import UserInDB
from shared.core.config import API_PREFIX
import shared.utils.repository_utils as ru
from shared.utils.short_pagination import short_pagination

class RawMaterialService:
    def __init__(self, db: Database):
        self.db = db

    async def create_raw_material(
        self, raw_material: RawMaterialCreate, current_user: UserInDB):

        new_raw_material = RawMaterialToSave(**raw_material.dict())
        new_raw_material.created_by = current_user.id
        new_raw_material.updated_by = uuid.UUID(int=0)

        raw_material_item = await RawMaterialRepository(self.db).create_raw_material(new_raw_material)

        if not raw_material_item:
            logger.error("Error creating raw material")
            return ServiceResult(RawMaterialExceptions.RawMaterialCreateException())

        return ServiceResult(raw_material_item)
    
    async def get_raw_material_list(
        self,
        search: str | None,
        page_num: int = 1,
        page_size: int = 10,
        order: str = None,
        direction: str = None,
    ) -> ServiceResult:
        raw_materials = await RawMaterialRepository(self.db).get_raw_material_list(search, order, direction)

        service_result = None
        if len(raw_materials) == 0:
            service_result = ServiceResult([])
            service_result.status_code = 204
        else:
            response = short_pagination(
                page_num=page_num,
                page_size=page_size,
                data_list=raw_materials,
                route=f"{API_PREFIX}/raw_materials",
            )
            service_result = ServiceResult(response)

        return service_result
    
    async def get_raw_material_by_id(self, id: UUID) -> ServiceResult:
        raw_material_in_db = await RawMaterialRepository(self.db).get_raw_material_by_id(id=id)

        if isinstance(raw_material_in_db, dict) and not raw_material_in_db.get("id"):
            logger.info("The requested raw material is not in the database")
            return ServiceResult(RawMaterialExceptions.RawMaterialNotFoundException())

        raw_material = RawMaterialInDB(**raw_material_in_db.dict())
        return ServiceResult(raw_material)
    
    async def update_raw_material(
        self, id: UUID, raw_material_update: RawMaterialUpdate, current_user: UserInDB
    ) -> ServiceResult:
        if not is_valid_uuid(id):
            return ServiceResult(RawMaterialExceptions.RawMaterialIdNoValidException())

        try:
            raw_material = await RawMaterialRepository(self.db).update_raw_material(
                id=id,
                raw_material_update=raw_material_update,
                updated_by_id=current_user.id,
            )

            if isinstance(raw_material, dict) and not raw_material.get("id"):
                logger.info("The raw material ID to update is not in the database")
                return ServiceResult(RawMaterialExceptions.RawMaterialNotFoundException())

            return ServiceResult(RawMaterialInDB(**raw_material.dict()))

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return ServiceResult(RawMaterialExceptions.RawMaterialInvalidUpdateParamsException(e))
    
    async def delete_raw_material_by_id(
        self, id: UUID
    ) -> ServiceResult:
        
        raw_material_id = await RawMaterialRepository(self.db).delete_raw_material_by_id(id=id)

        if isinstance(raw_material_id, dict) and not raw_material_id.get("id"):
            logger.info("The raw material ID to delete is not in the database")
            return ServiceResult(RawMaterialExceptions.RawMaterialNotFoundException())
        
        return ServiceResult(raw_material_id)