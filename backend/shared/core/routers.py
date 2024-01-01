from fastapi import APIRouter
from modules.users import users_router
from modules.warehouse.warehouse_routes import warehouse_router

router = APIRouter()

router.include_router(users_router)
router.include_router(warehouse_router)
