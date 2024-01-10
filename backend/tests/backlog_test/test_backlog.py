import uuid
import pytest

from fastapi import FastAPI, status
from loguru import logger
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

class TestBacklogCreateRoutes:
    async def test_create_backlog_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.post(app.url_path_for("backlog:create-backlog"), json={})
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestBacklogCreate:
    async def test_create_backlog_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        
        product = await client.post(app.url_path_for("product:create-product"), json={"product": {"name": "string","description": "string"}})
        product_list_response = await client.get(app.url_path_for("product:product_list"))
        product_list = product_list_response.json().get("data")[0]
        product_id = product_list.get("id")
        
        json = {
            "backlog": {
                "product_id": product_id,
                "required_quantity": 0
            }
        }

        res = await client.post(app.url_path_for("backlog:create-backlog"), json=json)
        assert res.status_code == status.HTTP_201_CREATED
        
class TestBacklogGetByListRoutes:
    async def test_backlog_list_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("backlog:backlog_list"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestBacklogList:
    async def test_backlog_list_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        res = await client.get(app.url_path_for("backlog:backlog_list"))
        assert res.status_code == status.HTTP_200_OK   
             
class TestBacklogGetRoutes:
    async def test_backlog_by_id_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("backlog:get-backlog-by-id", id="123e4567-e89b-12d3-a456-426614174000"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestBacklogGetById:
    async def test_backlog_by_id_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        
        product_list_response = await client.get(app.url_path_for("product:product_list"))
        product_list = product_list_response.json().get("data")[0]
        product_id = product_list.get("id")
        
        json = {
            "backlog": {
                "product_id": product_id,
                "required_quantity": 0
            }
        }

        backlog = await client.post(app.url_path_for("backlog:create-backlog"), json=json)
        backlog_list_response = await client.get(app.url_path_for("backlog:backlog_list"))
        backlog_list = backlog_list_response.json().get("data")[0]
        backlog_id = backlog_list.get("id")
        
        res = await client.get(app.url_path_for("backlog:get-backlog-by-id", id=backlog_id))
        assert res.status_code == status.HTTP_200_OK
        
class TestBacklogUpdateRoutes:
    async def test_backlog_update_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("backlog:update-backlog-by-id", id="123e4567-e89b-12d3-a456-426614174000"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestBacklogUpdateById:
    async def test_backlog_update_by_id_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        
        product_list_response = await client.get(app.url_path_for("product:product_list"))
        product_list = product_list_response.json().get("data")[0]
        product_id = product_list.get("id")
        
        
    
        backlog_list_response = await client.get(app.url_path_for("backlog:backlog_list"))
        backlog_list = backlog_list_response.json().get("data")[0]
        backlog_id = backlog_list.get("id")
        
        json = {
            "backlog_update": {
                "product_id": product_id,
                "required_quantity": 0,
                "is_active": True
  }
        }
        res = await client.put(app.url_path_for("backlog:update-backlog-by-id", id=backlog_id), json=json)
        assert res.status_code == status.HTTP_200_OK
        
        
class TestBacklogDeleteRoutes:
    async def test_backlog_delete_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.delete(app.url_path_for("backlog:delete-backlog-by-id", id="123e4567-e89b-12d3-a456-426614174000"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestBacklogDeleteById:
    async def test_backlog_delete_by_id_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        
        backlog_list_response = await client.get(app.url_path_for("backlog:backlog_list"))
        backlog_list = backlog_list_response.json().get("data")[0]
        backlog_id = backlog_list.get("id")
        res = await client.delete(app.url_path_for("backlog:delete-backlog-by-id", id=backlog_id))
        assert res.status_code == status.HTTP_200_OK