from fastapi import APIRouter
from modules.users import users_router
from modules.warehouse.warehouse_routes import warehouse_router
from modules.product.product_routes import product_router
from modules.raw_material.raw_material_routes import raw_material_router


router = APIRouter()

router.include_router(users_router)
router.include_router(warehouse_router)
router.include_router(product_router)
router.include_router(raw_material_router)
