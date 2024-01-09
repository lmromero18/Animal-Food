import uuid
import pytest

from fastapi import FastAPI, status
from loguru import logger
from httpx import AsyncClient
from modules.supplier.supplier_schemas import SupplierCreate, SupplierInDB, SupplierUpdate
from modules.supplier.supplier_schemas import (SupplierCreate)


pytestmark = pytest.mark.asyncio

class TestSupplierCreateRoutes:
    async def test_create_supplier_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.post(app.url_path_for("supplier:create-supplier"), json={})
        assert res.status_code != status.HTTP_404_NOT_FOUND

class TestSupplierCreate:
    async def test_create_supplier_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        res = await client.post(app.url_path_for("supplier:create-supplier"), json={"supplier": {"name": "string","address": "string"}})
        assert res.status_code == status.HTTP_201_CREATED

class TestSupplierGeByListRoutes:
    async def test_supplier_list_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("supplier:supplier_list"))
        assert res.status_code != status.HTTP_404_NOT_FOUND

class TestSupplierList:
    async def test_supplier_list_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        res = await client.get(app.url_path_for("supplier:supplier_list"))
        assert res.status_code == status.HTTP_200_OK  

class TestSupplierGetRoutes:
    async def test_supplier_by_id_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("supplier:get-supplier-by-id", id="123e4567-e89b-12d3-a456-426614174000"))
        assert res.status_code != status.HTTP_404_NOT_FOUND      