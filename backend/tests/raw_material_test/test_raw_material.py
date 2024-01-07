import uuid
import pytest

from fastapi import FastAPI, status
from loguru import logger
from httpx import AsyncClient
from modules.raw_material.raw_material_schemas import RawMaterialCreate, RawMaterialInDB, RawMaterialUpdate

from modules.raw_material.raw_material_schemas import(RawMaterialCreate)

pytestmark = pytest.mark.asyncio

class TestRawMaterialCreateRoutes:
    async def test_create_raw_material_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.post(app.url_path_for("raw_material:create-raw-material"), json={})
        assert res.status_code != status.HTTP_404_NOT_FOUND

class TestRawMaterialCreate:
    async def test_create_raw_material_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        warehouse = await client.post(app.url_path_for("warehouse:create-warehouse"), json={"warehouse": {"type": "test"}})
        warehouse_list_response = await client.get(app.url_path_for("warehouse:warehouse_list"))
        warehouse_list = warehouse_list_response.json().get("data")[0]
        warehouse_id = warehouse_list.get("id")
        res = await client.post(app.url_path_for("raw_material:create-raw-material"), json={"raw_material": {"name": "string","code": "string","available_quantity": 0,"warehouse_id": warehouse_id}})
        assert res.status_code == status.HTTP_201_CREATED
            