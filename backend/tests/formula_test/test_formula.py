import uuid
import pytest

from fastapi import FastAPI, status
from loguru import logger
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

class TestFormulaCreateRoutes:
    async def test_create_formula_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.post(app.url_path_for("formula:create-formula"), json={})
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestFormulaCreate:
    async def test_create_formula_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client

        product_json = {
            "product": {
                "name": "string",
                "description": "string"
            }
        }

        product = await client.post(app.url_path_for("product:create-product"), json=product_json)
        assert product.status_code == status.HTTP_201_CREATED
        product_list_response = await client.get(app.url_path_for("product:product_list"))
        product_list = product_list_response.json().get("data")[0]
        product_id = product_list.get("id")
        
        warehouse = await client.post(app.url_path_for("warehouse:create-warehouse"), json={"warehouse": {"type": "test"}})
        warehouse_list_response = await client.get(app.url_path_for("warehouse:warehouse_list"))
        warehouse_list = warehouse_list_response.json().get("data")[0]
        warehouse_id = warehouse_list.get("id")
        
        raw_material = await client.post(app.url_path_for("raw_material:create-raw-material"), json={"raw_material": {"name": "string","code": "string","available_quantity": 20,"warehouse_id": warehouse_id}})
        assert raw_material.status_code == status.HTTP_201_CREATED
        raw_material_list_response = await client.get(app.url_path_for("raw_material:raw_material_list"))
        raw_material_list = raw_material_list_response.json().get("data")[0]
        raw_material_id = raw_material_list.get("id")

        json_formula = {
            "formula": {
                "required_quantity": 1,
                "product_id": product_id,
                "raw_material_id": raw_material_id
            }
        }

        res = await client.post(app.url_path_for("formula:create-formula"), json=json_formula)
        assert res.status_code == status.HTTP_201_CREATED
        
class TestFormulaGetByListRoutes:
    async def test_formula_list_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("formula:formula-list"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestFormulaList:
    async def test_formula_list_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        res = await client.get(app.url_path_for("formula:formula-list"))
        assert res.status_code == status.HTTP_200_OK
        
class TestFormulaGetRoutes:
    async def test_formula_by_id_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("formula:get-formula-by-id", id="123e4567-e89b-12d3-a456-426614174000"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestFormulaGetById:
    async def test_get_formula_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client

        product_list_response = await client.get(app.url_path_for("product:product_list"))
        product_list = product_list_response.json().get("data")[0]
        product_id = product_list.get("id")
        
        warehouse = await client.post(app.url_path_for("warehouse:create-warehouse"), json={"warehouse": {"type": "test"}})
        warehouse_list_response = await client.get(app.url_path_for("warehouse:warehouse_list"))
        warehouse_list = warehouse_list_response.json().get("data")[0]
        warehouse_id = warehouse_list.get("id")
        
        raw_material_list_response = await client.get(app.url_path_for("raw_material:raw_material_list"))
        raw_material_list = raw_material_list_response.json().get("data")[0]
        raw_material_id = raw_material_list.get("id")

        json_formula = {
            "formula": {
                "required_quantity": 1,
                "product_id": product_id,
                "raw_material_id": raw_material_id
            }
        }

        formula_list_response = await client.get(app.url_path_for("formula:formula-list"))
        formula_list = formula_list_response.json().get("data")[0]
        formula_id = formula_list.get("id")
        
        res = await client.get(app.url_path_for("formula:get-formula-by-id", id=formula_id))
        assert res.status_code == status.HTTP_200_OK
        
class TestFormulaUpdateRoutes:
    async def test_formula_update_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("formula:update-formula-by-id", id="123e4567-e89b-12d3-a456-426614174000"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
        
class TestFormulaUpdateById:
    async def test_formula_update_by_id_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        
        product_json = {
            "product": {
                "name": "string",
                "description": "string"
  }
        }
        
        product_list_response = await client.get(app.url_path_for("product:product_list"))
        product_list = product_list_response.json().get("data")[0]
        product_id = product_list.get("id")
        
        warehouse = await client.post(app.url_path_for("warehouse:create-warehouse"), json={"warehouse": {"type": "test"}})
        warehouse_list_response = await client.get(app.url_path_for("warehouse:warehouse_list"))
        warehouse_list = warehouse_list_response.json().get("data")[0]
        warehouse_id = warehouse_list.get("id")
        
        raw_material_list_response = await client.get(app.url_path_for("raw_material:raw_material_list"))
        raw_material_list = raw_material_list_response.json().get("data")[0]
        raw_material_id = raw_material_list.get("id")  
        

        
    
        formula_list_response = await client.get(app.url_path_for("formula:formula-list"))
        formula_list = formula_list_response.json().get("data")[0]
        formula_id = formula_list.get("id")
        
        formula_update_json = {
            
            "formula_update": {
                "required_quantity": 1,
                "product_id": product_id,
                "raw_material_id": raw_material_id,
                "is_active": True
            }
            
        }
        
        res = await client.put(app.url_path_for("formula:update-formula-by-id", id=formula_id), json=formula_update_json)
        assert res.status_code == status.HTTP_200_OK
        
class TestFormulaDeleteRoutes:
    async def test_formula_delete_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.delete(app.url_path_for("formula:delete-formula-by-id", id="123e4567-e89b-12d3-a456-426614174000"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestFormulaDeleteById:
    async def test_formula_delete_by_id_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        formula_list_response = await client.get(app.url_path_for("formula:formula-list"))
        formula_list = formula_list_response.json().get("data")[0]
        formula_id = formula_list.get("id")
        
        res = await client.delete(app.url_path_for("formula:delete-formula-by-id", id=formula_id))
        assert res.status_code == status.HTTP_200_OK 