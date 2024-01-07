import uuid
import pytest

from fastapi import FastAPI, status
from loguru import logger
from httpx import AsyncClient
from modules.warehouse.warehouse_schemas import WarehouseCreate, WarehouseInDB, WarehouseUpdate

from modules.warehouse.warehouse_schemas import (
    WarehouseCreate
)

pytestmark = pytest.mark.asyncio

class TestWarehouseCreateRoutes:
    async def test_create_warehouse_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.post(app.url_path_for("warehouse:create-warehouse"), json={})
        assert res.status_code != status.HTTP_404_NOT_FOUND

class TestWarehouseCreate:
    async def test_create_warehouse_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        res = await client.post(app.url_path_for("warehouse:create-warehouse"), json={"warehouse": {"type": "test"}})
        assert res.status_code == status.HTTP_201_CREATED
    

class TestWarehouseGeByListRoutes:
    async def test_warehouse_list_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("warehouse:warehouse_list"))
        assert res.status_code != status.HTTP_404_NOT_FOUND

class TestWarehouseList:
    async def test_warehouse_list_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        res = await client.get(app.url_path_for("warehouse:warehouse_list"))
        assert res.status_code == status.HTTP_200_OK

class TestWarehouseGetRoutes:
    async def test_warehouse_by_id_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("warehouse:get-warehouse-by-id", id="123e4567-e89b-12d3-a456-426614174000"))
        assert res.status_code != status.HTTP_404_NOT_FOUND

#este hay que revisarlo
#class TestWarehouseGetById:
    #async def test_warehouse_by_id_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        #client = await authorized_client
        #res = await client.get(app.url_path_for("warehouse:get-warehouse-by-id", id="1"))
        #assert res.status_code == status.HTTP_200_OK


      

