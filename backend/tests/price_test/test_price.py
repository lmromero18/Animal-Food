import uuid
import pytest

from fastapi import FastAPI, status
from loguru import logger
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestPriceCreateRoutes:
    async def test_create_price_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.post(app.url_path_for("price:create-price"), json={})
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestPriceCreate:
    async def test_create_price_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        
        product = await client.post(app.url_path_for("product:create-product"), json={"product": {"name": "string","description": "string"}})
        product_list_response = await client.get(app.url_path_for("product:product_list"))
        product_list = product_list_response.json().get("data")[0]
        product_id = product_list.get("id")
        
        json = {
        "price": {
            "price": 20,
            "product_id": product_id
        }
        }
        res = await client.post(app.url_path_for("price:create-price"), json=json)
        assert res.status_code == status.HTTP_201_CREATED
        
class TestPriceGetByListRoutes:
    async def test_price_list_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("price:price_list"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestPriceList:
    async def test_price_list_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        res = await client.get(app.url_path_for("price:price_list"))
        assert res.status_code == status.HTTP_200_OK
        
class TestPriceGetRoutes:
    async def test_price_by_id_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("price:get-price-by-id", id="123e4567-e89b-12d3-a456-426614174000"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestPriceGetById:
    async def test_price_by_id_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        
        product_list_response = await client.get(app.url_path_for("product:product_list"))
        product_list = product_list_response.json().get("data")[0]
        product_id = product_list.get("id")
        
        json = {
        "price": {
            "price": 20,
            "product_id": product_id
        }
        }
        price = await client.post(app.url_path_for("price:create-price"), json=json)
        price_list_response = await client.get(app.url_path_for("price:price_list"))
        price_list = price_list_response.json().get("data")[0]
        price_id = price_list.get("id")
        res = await client.get(app.url_path_for("price:get-price-by-id", id=price_id))
        assert res.status_code == status.HTTP_200_OK
        
class TestPriceUpdateRoutes:
    async def test_price_update_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("price:update-price-by-id", id="123e4567-e89b-12d3-a456-426614174000"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestPriceUpdateById:
    async def test_price_update_by_id_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        
        product_list_response = await client.get(app.url_path_for("product:product_list"))
        product_list = product_list_response.json().get("data")[0]
        product_id = product_list.get("id")
        
        json = {
        "price": {
            "price": 20,
            "product_id": product_id
        }
        }
        price = await client.post(app.url_path_for("price:create-price"), json=json)
        price_list_response = await client.get(app.url_path_for("price:price_list"))
        price_list = price_list_response.json().get("data")[0]
        price_id = price_list.get("id")
        res = await client.put(app.url_path_for("price:update-price-by-id", id=price_id), json={"price": {"price": 20,"product_id": product_id}})
        assert res.status_code != status.HTTP_200_OK
        
class TestPriceDeleteRoutes:
    async def test_price_delete_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.delete(app.url_path_for("price:delete-price-by-id", id="123e4567-e89b-12d3-a456-426614174000"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestPriceDeleteById:
    async def test_price_delete_by_id_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        
        product_list_response = await client.get(app.url_path_for("product:product_list"))
        product_list = product_list_response.json().get("data")[0]
        product_id = product_list.get("id")
        
        json = {
        "price": {
            "price": 20,
            "product_id": product_id
        }
        }
        price = await client.post(app.url_path_for("price:create-price"), json=json)
        price_list_response = await client.get(app.url_path_for("price:price_list"))
        price_list = price_list_response.json().get("data")[0]
        price_id = price_list.get("id")
        res = await client.delete(app.url_path_for("price:delete-price-by-id", id=price_id))
        assert res.status_code == status.HTTP_200_OK