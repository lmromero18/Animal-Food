import pytest

from fastapi import FastAPI, status
from loguru import logger
from httpx import AsyncClient
from modules.warehouse.warehouse_schemas import WarehouseCreate

from modules.warehouse.warehouse_schemas import (
    WarehouseCreate
)

pytestmark = pytest.mark.asyncio

class TestWarehouseRoutes:
    async def test_create_warehouse_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.post(app.url_path_for("warehouse:create-warehouse"), json={})
        assert res.status_code != status.HTTP_404_NOT_FOUND

class TestWarehouseCreate:
    async def test_create_warehouse_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        res = await client.post(app.url_path_for("warehouse:create-warehouse"), json={"warehouse": {"type": "test"}})
        assert res.status_code == status.HTTP_201_CREATED
    