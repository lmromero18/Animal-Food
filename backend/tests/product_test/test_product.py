import uuid
import pytest

from fastapi import FastAPI, status
from loguru import logger
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

class TestProductCreateRoutes:
    async def test_create_product_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.post(app.url_path_for("product:create-product"), json={})
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestProductCreate:
    async def test_create_product_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        res = await client.post(app.url_path_for("product:create-product"), json={"product": {"name": "string","description": "string"}})
        assert res.status_code == status.HTTP_201_CREATED
        
class TestProductGetByListRoutes:
    async def test_product_list_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("product:product_list"))
        assert res.status_code != status.HTTP_404_NOT_FOUND

class TestProductList:
    async def test_product_list_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        res = await client.get(app.url_path_for("product:product_list"))
        assert res.status_code == status.HTTP_200_OK
        
class TestProductGetRoutes:
    async def test_product_by_id_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("product:get-product-by-id", id="123e4567-e89b-12d3-a456-426614174000"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestProductGetById:
    async def test_product_by_id_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        product = await client.post(app.url_path_for("product:create-product"), json={"product": {"name": "ProductName","description": "string"}})
        product_list_response = await client.get(app.url_path_for("product:product_list"))
        product_list = product_list_response.json().get("data")[0]
        product_id = product_list.get("id")
        res = await client.get(app.url_path_for("product:get-product-by-id", id=product_id))
        assert res.status_code == status.HTTP_200_OK
        
class TestProductUpdateRoutes:
    async def test_product_update_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("product:update-product-by-id", id="123e4567-e89b-12d3-a456-426614174000"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestProductUpdateById:
    async def test_product_update_by_id_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        product_list_response = await client.get(app.url_path_for("product:product_list"))
        product_list = product_list_response.json().get("data")[0]
        product_id = product_list.get("id")
        res = await client.put(app.url_path_for("product:update-product-by-id", id=product_id), json={"product_update": {"name": "ProductName","description": "string", "is_active": True}})
        assert res.status_code == status.HTTP_200_OK
        
class TestProductDeleteRoutes:
    async def test_product_delete_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.delete(app.url_path_for("product:delete-product-by-id", id="123e4567-e89b-12d3-a456-426614174000"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestProductDeleteById:
    async def test_product_delete_by_id_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        product_list_response = await client.get(app.url_path_for("product:product_list"))
        product_list = product_list_response.json().get("data")[0]
        product_id = product_list.get("id")
        res = await client.delete(app.url_path_for("product:delete-product-by-id", id=product_id))
        assert res.status_code == status.HTTP_200_OK
    
    
    