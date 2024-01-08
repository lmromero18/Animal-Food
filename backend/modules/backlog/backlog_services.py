from typing import List
from uuid import UUID
import uuid
from shared.utils.record_to_dict import record_to_dict
from shared.utils.verify_uuid import is_valid_uuid


from databases import Database
import fastapi
from loguru import logger

from shared.utils.service_result import ServiceResult
from modules.backlog.backlog_repositories import BacklogRepository
from modules.backlog.backlog_exceptions import BacklogExceptions
from modules.backlog.backlog_schemas import (
    BacklogCreate,
    BacklogToSave,
    BacklogInDB,
    BacklogUpdate
)
from modules.users.users.user_schemas import UserInDB
from shared.core.config import API_PREFIX
import shared.utils.repository_utils as ru
from shared.utils.short_pagination import short_pagination

class BacklogService:
    def __init__(self, db: Database):
        self.db = db

    async def create_backlog(
    self, backlog: BacklogCreate, current_user: UserInDB):

        new_backlog = BacklogToSave(**backlog.dict())
        new_backlog.created_by = current_user.id
        new_backlog.updated_by = uuid.UUID(int=0)

        backlog_item = await BacklogRepository(self.db).create_backlog(new_backlog)

        if not backlog_item:
            logger.error("Error creating backlog")
            return ServiceResult(BacklogExceptions.BacklogCreateException())

        return ServiceResult(backlog_item)
    
    async def get_backlog_list(
        self,
        search: str | None,
        page_num: int = 1,
        page_size: int = 10,
        order: str = None,
        direction: str = None,
    ) -> ServiceResult:
        backlog = await BacklogRepository(self.db).get_backlog_list(search, order, direction)

        service_result = None
        if len(backlog) == 0:
            service_result = ServiceResult([])
            service_result.status_code = 204
        else:
            response = short_pagination(
                page_num=page_num,
                page_size=page_size,
                data_list=backlog,
                route=f"{API_PREFIX}/backlog",
            )
            service_result = ServiceResult(response)

        return service_result
    
    async def get_backlog_by_id(self, id: UUID) -> ServiceResult:
        backlog_in_db = await BacklogRepository(self.db).get_backlog_by_id(id=id)

        if isinstance(backlog_in_db, dict) and not backlog_in_db.get("id"):
            logger.info("El backlog solicitado no está en base de datos")
            return ServiceResult(BacklogExceptions.BacklogNotFoundException())

        backlog = BacklogInDB(**backlog_in_db.dict())
        return ServiceResult(backlog)
    
    async def update_backlog(
        self, id: UUID, backlog_update: BacklogUpdate, current_user: UserInDB
    ) -> ServiceResult:
        if not is_valid_uuid(id):
            return ServiceResult(BacklogExceptions.BacklogIdNoValidException())

        try:
            backlog = await BacklogRepository(self.db).update_backlog(
                id=id,
                backlog_update=backlog_update,
                updated_by_id=current_user.id,
            )

            if isinstance(backlog, dict) and not backlog.get("id"):
                logger.info("El ID del backlog a actualizar no está en base de datos")
                return ServiceResult(BacklogExceptions.BacklogNotFoundException())

            return ServiceResult(BacklogInDB(**backlog.dict()))

        except Exception as e:
            logger.error(f"Se produjo un error: {e}")
            return ServiceResult(BacklogExceptions.BacklogInvalidUpdateParamsException(e))
    
    async def delete_backlog_by_id(
        self, id: UUID
    ) -> ServiceResult:
        
        backlog_id = await BacklogRepository(self.db).delete_backlog_by_id(id=id)

        if isinstance(backlog_id, dict) and not backlog_id.get("id"):
                logger.info("El ID de tarea a eliminar no está en base de datos")
                return ServiceResult(BacklogExceptions.BacklogNotFoundException())
        
        return  ServiceResult(backlog_id)
