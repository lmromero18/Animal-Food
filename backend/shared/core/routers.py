from fastapi import APIRouter
from modules.users import users_router
from modules.warehouse.warehouse_routes import warehouse_router
from modules.price.price_routes import price_router
from modules.product.product_routes import product_router
from modules.raw_material.raw_material_routes import raw_material_router
from modules.formula.formula_routes import formula_router
from modules.product_offered.product_offered_routes import product_offered_router
from modules.supplier.supplier_routes import supplier_router
from modules.purchase.purchase_routes import purchase_router



router = APIRouter()

router.include_router(users_router)
router.include_router(warehouse_router)
router.include_router(price_router)
router.include_router(product_router)
router.include_router(product_offered_router)
router.include_router(raw_material_router)
router.include_router(formula_router)
router.include_router(supplier_router)
router.include_router(purchase_router)
