import uuid
import pytest

from fastapi import FastAPI, status
from loguru import logger
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

class TestOrderCreateRoutes:
    async def test_create_order_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.post(app.url_path_for("order:create-order"), json={})
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestOrderCreate:
    async def test_create_order_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client       

        product = await client.post(app.url_path_for("product:create-product"), json={"product": {"name": "ProductName98989","description": "string"}})
        product_list_response = await client.get(app.url_path_for("product:product_list"))
        product_list = product_list_response.json().get("data")[0]
        product_id = product_list['id']
        
        json = {
            "price": {
                "price": 20,
                "product_id": product_id
            }
        }
        
        price = await client.post(app.url_path_for("price:create-price"), json=json)
        assert price.status_code == status.HTTP_201_CREATED             
        
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
        product_offered = await client.post(app.url_path_for("product-offered:create-product-offered"), json=json)
        assert product_offered.status_code == status.HTTP_201_CREATED
        #get product offered id
        product_offered_list_response = await client.get(app.url_path_for("product-offered:product-offered-list"))
        product_offered_list = product_offered_list_response.json().get("data")[0]
        product_offered_id = product_offered_list.get("id")
        
        order_json = {
            "order": {
                "product_offered_id": product_offered_id,
                "quantity": 1,
                "discount": 0
            }
        }
        
        res = await client.post(app.url_path_for("order:create-order"), json=order_json)
        assert res.status_code == status.HTTP_201_CREATED
        
class TestOrderGetByListRoutes:
    async def test_order_list_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("order:order_list"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestOrderList:
    async def test_order_list_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        res = await client.get(app.url_path_for("order:order_list"))
        assert res.status_code == status.HTTP_200_OK
        
class TestOrderGetRoutes:
    async def test_order_by_id_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("order:get-order-by-id", id="123e4567-e89b-12d3-a456-426614174000"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestOrderGetById:
    async def test_order_by_id_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        
        product_list_response = await client.get(app.url_path_for("product:product_list"))
        product_list = product_list_response.json().get("data")[0]
        product_id = product_list['id']
           
        
        warehouse = await client.post(app.url_path_for("warehouse:create-warehouse"), json={"warehouse": {"type": "test"}})
        warehouse_list_response = await client.get(app.url_path_for("warehouse:warehouse_list"))
        warehouse_list = warehouse_list_response.json().get("data")[0]
        warehouse_id = warehouse_list.get("id")
        
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
        product_offered = await client.get(app.url_path_for("product-offered:product-offered-list"))
        product_offered_list = product_offered.json().get("data")[0]
        product_offered_id = product_offered_list.get("id")
        
        order_json = {
            "order_update": {
                "product_offered_id": product_offered_id,
                "quantity": 1,
                "discount": 0,
                "is_delivered": True
            }
            
        }
        
        order_list_response = await client.get(app.url_path_for("order:order_list"))
        order_list = order_list_response.json().get("data")[0]
        order_id = order_list.get("id")
        
        res = await client.get(app.url_path_for("order:get-order-by-id", id=order_id))
        assert res.status_code == status.HTTP_200_OK
        
class TestOrderUpdateRoutes:
    async def test_order_update_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("order:update-order-by-id", id="123e4567-e89b-12d3-a456-426614174000"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestOrderUpdateById:
    async def test_order_update_by_id_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        
        product_list_response = await client.get(app.url_path_for("product:product_list"))
        product_list = product_list_response.json().get("data")[0]
        product_id = product_list['id']
           
        
        warehouse = await client.post(app.url_path_for("warehouse:create-warehouse"), json={"warehouse": {"type": "test"}})
        warehouse_list_response = await client.get(app.url_path_for("warehouse:warehouse_list"))
        warehouse_list = warehouse_list_response.json().get("data")[0]
        warehouse_id = warehouse_list.get("id")
        
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
        product_offered = await client.get(app.url_path_for("product-offered:product-offered-list"))
        product_offered_list = product_offered.json().get("data")[0]
        product_offered_id = product_offered_list.get("id")
        
        order_json = {
            "order_update": {
                "product_offered_id": product_offered_id,
                "quantity": 1,
                "discount": 0,
                "is_delivered": True
            }
            
        }
        
        order_list_response = await client.get(app.url_path_for("order:order_list"))
        order_list = order_list_response.json().get("data")[0]
        order_id = order_list.get("id")
        
        res = await client.put(app.url_path_for("order:update-order-by-id", id=order_id), json=order_json)
        assert res.status_code == status.HTTP_200_OK
        
class TestOrderDeleteRoutes:
    async def test_order_delete_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("order:delete-order-by-id", id="123e4567-e89b-12d3-a456-426614174000"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestOrderDeleteById:
    async def test_order_delete_by_id_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        
        product_list_response = await client.get(app.url_path_for("product:product_list"))
        product_list = product_list_response.json().get("data")[0]
        product_id = product_list['id']
           
        
        warehouse = await client.post(app.url_path_for("warehouse:create-warehouse"), json={"warehouse": {"type": "test"}})
        warehouse_list_response = await client.get(app.url_path_for("warehouse:warehouse_list"))
        warehouse_list = warehouse_list_response.json().get("data")[0]
        warehouse_id = warehouse_list.get("id")
        
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
        product_offered = await client.get(app.url_path_for("product-offered:product-offered-list"))
        product_offered_list = product_offered.json().get("data")[0]
        product_offered_id = product_offered_list.get("id")
        
        order_json = {
            "order_update": {
                "product_offered_id": product_offered_id,
                "quantity": 1,
                "discount": 0,
                "is_delivered": True
            }
            
        }
        
        order_list_response = await client.get(app.url_path_for("order:order_list"))
        order_list = order_list_response.json().get("data")[0]
        order_id = order_list.get("id")
        
        res = await client.delete(app.url_path_for("order:delete-order-by-id", id=order_id))
        assert res.status_code == status.HTTP_200_OK
            
        
        
        
        
            
        
        
        
        