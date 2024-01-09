import uuid
import pytest

from fastapi import FastAPI, status
from loguru import logger
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

class TestProductOfferedCreateRoutes:
    async def test_create_product_offered_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.post(app.url_path_for("product-offered:create-product-offered"), json={})
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestProductOfferedCreate:
    async def test_create_product_offered_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        
        product = await client.post(app.url_path_for("product:create-product"), json={"product": {"name": "ProductName98989","description": "string"}})
        product_list_response = await client.get(app.url_path_for("product:product_list"))
        product_list = product_list_response.json().get("data")[0]
        product_id = product_list['id']
               
        
        warehouse = await client.post(app.url_path_for("warehouse:create-warehouse"), json={"warehouse": {"type": "test"}})
        warehouse_list_response = await client.get(app.url_path_for("warehouse:warehouse_list"))
        warehouse_list = warehouse_list_response.json().get("data")[0]
        warehouse_id = warehouse_list.get("id")
        
        raw_material = await client.post(app.url_path_for("raw_material:create-raw-material"), json={"raw_material": {"name": "string564654","code": "string564654","available_quantity": 450,"warehouse_id": warehouse_id}})
        raw_material_list_response = await client.get(app.url_path_for("raw_material:raw_material_list"))
        raw_material_list = raw_material_list_response.json().get("data")[0]
        raw_material_id = raw_material_list.get("id")
                
        formula_json = {
            "formula": {
                "required_quantity": 1,
                "product_id": product_id,
                "raw_material_id": raw_material_id
            }
        }
        formula = await client.post(app.url_path_for("formula:create-formula"), json=formula_json)
        assert formula.status_code == status.HTTP_201_CREATED
        
        json = {
            "product": {
                "quantity": 20,                
                "product_id": product_id,
                "warehouse_id": warehouse_id,
            }
        }
        res = await client.post(app.url_path_for("product-offered:create-product-offered"), json=json)
        assert res.status_code == status.HTTP_201_CREATED

class TestProductOfferedList:
    async def test_product_offered_list_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("product-offered:product-offered-list"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestProductOfferedListRoute:
    async def test_product_offered_list_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        res = await client.get(app.url_path_for("product-offered:product-offered-list"))
        assert res.status_code == status.HTTP_200_OK
        
class TestProductOfferedGetRoutes:
    async def test_product_offered_by_id_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("product-offered:get-product-offered-by-id", id="123e4567-e89b-12d3-a456-426614174000"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestProductOfferedGetById:
    async def test_product_offered_by_id_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        
        product_list_response = await client.get(app.url_path_for("product:product_list"))
        product_list = product_list_response.json().get("data")[0]
        product_id = product_list['id']
               
        
        warehouse_list_response = await client.get(app.url_path_for("warehouse:warehouse_list"))
        warehouse_list = warehouse_list_response.json().get("data")[0]
        warehouse_id = warehouse_list.get("id")
        
        raw_material = await client.post(app.url_path_for("raw_material:create-raw-material"), json={"raw_material": {"name": "string564654","code": "string564654","available_quantity": 450,"warehouse_id": warehouse_id}})
        raw_material_list_response = await client.get(app.url_path_for("raw_material:raw_material_list"))
        raw_material_list = raw_material_list_response.json().get("data")[0]
        raw_material_id = raw_material_list.get("id")
                
        formula_json = {
            "formula": {
                "required_quantity": 1,
                "product_id": product_id,
                "raw_material_id": raw_material_id
            }
        }
        formula = await client.post(app.url_path_for("formula:create-formula"), json=formula_json)
        
        json = {
            "product": {
                "quantity": 20,                
                "product_id": product_id,
                "warehouse_id": warehouse_id,
            }
        }
        product_offered = await client.post(app.url_path_for("product-offered:create-product-offered"), json=json)
        product_offered_list_response = await client.get(app.url_path_for("product-offered:product-offered-list"))
        product_offered_list = product_offered_list_response.json().get("data")[0]
        product_offered_id = product_offered_list.get("id")
        res = await client.get(app.url_path_for("product-offered:get-product-offered-by-id", id=product_offered_id))
        assert res.status_code == status.HTTP_200_OK
        
class TestProductOfferedUpdateRoutes:
    async def test_product_offered_update_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("product-offered:update-product-offered-by-id", id="123e4567-e89b-12d3-a456-426614174000"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestProductOfferedUpdateById:
    async def test_product_offered_update_by_id_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        
        product = await client.post(app.url_path_for("product:create-product"), json={"product": {"name": "ProductName98989897987987","description": "string"}})
        product_list_response = await client.get(app.url_path_for("product:product_list"))
        product_list = product_list_response.json().get("data")[0]
        product_id = product_list['id']
               
        
        warehouse = await client.post(app.url_path_for("warehouse:create-warehouse"), json={"warehouse": {"type": "test"}})
        warehouse_list_response = await client.get(app.url_path_for("warehouse:warehouse_list"))
        warehouse_list = warehouse_list_response.json().get("data")[0]
        warehouse_id = warehouse_list.get("id")
        
        raw_material = await client.post(app.url_path_for("raw_material:create-raw-material"), json={"raw_material": {"name": "string564654","code": "string564654","available_quantity": 450,"warehouse_id": warehouse_id}})
        raw_material_list_response = await client.get(app.url_path_for("raw_material:raw_material_list"))
        raw_material_list = raw_material_list_response.json().get("data")[0]
        raw_material_id = raw_material_list.get("id")
                
        formula_json = {
            "formula": {
                "required_quantity": 1,
                "product_id": product_id,
                "raw_material_id": raw_material_id
            }
        }
        formula = await client.post(app.url_path_for("formula:create-formula"), json=formula_json)
        assert formula.status_code == status.HTTP_201_CREATED

        product_offered_list_response = await client.get(app.url_path_for("product-offered:product-offered-list"))
        product_offered_list = product_offered_list_response.json().get("data")[0]
        product_offered_id = product_offered_list.get("id")
        
        product_offered_update = {
            "product_offered_update": {
                "quantity": 0,
                "product_id": product_id,
                "warehouse_id": warehouse_id,
                "name": "JKHkfjasdhkfasdjh",
                "is_active": True
            }
        }
        res = await client.put(app.url_path_for("product-offered:update-product-offered-by-id", id=product_offered_id), json=product_offered_update)
        assert res.status_code == status.HTTP_200_OK
            
class TestProductOfferedDeleteRoutes:
    async def test_product_offered_delete_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.delete(app.url_path_for("product-offered:delete-product-offered-by-id", id="123e4567-e89b-12d3-a456-426614174000"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestProductOfferedDeleteById:
    async def test_product_offered_delete_by_id_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        
        product_list_response = await client.get(app.url_path_for("product:product_list"))
        product_list = product_list_response.json().get("data")[0]
        product_id = product_list['id']
               
        
        warehouse = await client.post(app.url_path_for("warehouse:create-warehouse"), json={"warehouse": {"type": "test"}})
        warehouse_list_response = await client.get(app.url_path_for("warehouse:warehouse_list"))
        warehouse_list = warehouse_list_response.json().get("data")[0]
        warehouse_id = warehouse_list.get("id")
        
        raw_material = await client.post(app.url_path_for("raw_material:create-raw-material"), json={"raw_material": {"name": "string564654","code": "string564654","available_quantity": 450,"warehouse_id": warehouse_id}})
        raw_material_list_response = await client.get(app.url_path_for("raw_material:raw_material_list"))
        raw_material_list = raw_material_list_response.json().get("data")[0]
        raw_material_id = raw_material_list.get("id")
                
        formula_json = {
            "formula": {
                "required_quantity": 1,
                "product_id": product_id,
                "raw_material_id": raw_material_id
            }
        }
        formula = await client.post(app.url_path_for("formula:create-formula"), json=formula_json)
        assert formula.status_code == status.HTTP_201_CREATED

        product_offered_list_response = await client.get(app.url_path_for("product-offered:product-offered-list"))
        product_offered_list = product_offered_list_response.json().get("data")[0]
        product_offered_id = product_offered_list.get("id")
        
        if product_offered_id:
            res = await client.delete(app.url_path_for("product-offered:delete-product-offered-by-id", id=product_offered_id))
            assert res.status_code == status.HTTP_200_OK
        