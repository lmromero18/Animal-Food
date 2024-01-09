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
        res = await client.post(app.url_path_for("raw_material:create-raw-material"), json={"raw_material": {"name": "string","code": "string","available_quantity": 20,"warehouse_id": warehouse_id}})
        assert res.status_code == status.HTTP_201_CREATED
        
class TestRawMaterialGetByListRoutes:
    async def test_raw_material_list_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("raw_material:raw_material_list"))
        assert res.status_code != status.HTTP_404_NOT_FOUND

class TestRawMaterialList:
    async def test_raw_material_list_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        res = await client.get(app.url_path_for("raw_material:raw_material_list"))
        assert res.status_code == status.HTTP_200_OK
            
class TestRawMaterialGetRoutes:
    async def test_raw_material_by_id_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("raw_material:get-raw-material-by-id", id="123e4567-e89b-12d3-a456-426614174000"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestRawMaterialGetById:
    async def test_raw_material_by_id_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        warehouse = await client.post(app.url_path_for("warehouse:create-warehouse"), json={"warehouse": {"type": "test"}})
        warehouse_list_response = await client.get(app.url_path_for("warehouse:warehouse_list"))
        warehouse_list = warehouse_list_response.json().get("data")[0]
        warehouse_id = warehouse_list.get("id")
        raw_material = await client.post(app.url_path_for("raw_material:create-raw-material"), json={"raw_material": {"name": "string","code": "string","available_quantity": 20,"warehouse_id": warehouse_id}})
        raw_material_list_response = await client.get(app.url_path_for("raw_material:raw_material_list"))
        raw_material_list = raw_material_list_response.json().get("data")[0]
        raw_material_id = raw_material_list.get("id")
        res = await client.get(app.url_path_for("raw_material:get-raw-material-by-id", id=raw_material_id))
        assert res.status_code == status.HTTP_200_OK
        
class TestRawMaterialUpdateRoutes:
    async def test_raw_material_update_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("raw_material:update-raw-material-by-id", id="123e4567-e89b-12d3-a456-426614174000"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
    
class TestRawMaterialUpdateById:
    async def test_raw_material_update_by_id_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        
        #Create a warehouse
        warehouse = await client.post(app.url_path_for("warehouse:create-warehouse"), json={"warehouse": {"type": "test"}})
        warehouse_list_response = await client.get(app.url_path_for("warehouse:warehouse_list"))
        warehouse_list = warehouse_list_response.json().get("data")[0]
        warehouse_id = warehouse_list.get("id")        
        
        #Create a raw material
        raw_material = await client.post(app.url_path_for("raw_material:create-raw-material"), json={"raw_material": {"name": "string2","code": "string2","available_quantity": 20,"warehouse_id": warehouse_id}})
        raw_material_list_response = await client.get(app.url_path_for("raw_material:raw_material_list"))
        raw_material_list = raw_material_list_response.json().get("data")[0]
        raw_material_id = raw_material_list.get("id")
        
        raw_material = await client.get(app.url_path_for("raw_material:get-raw-material-by-id", id=raw_material_id))
        
        # Update the raw material
        raw_material_update = {
        "raw_material_update": {
            "name": "string",
            "code": "string",
            "available_quantity": 40,
            "warehouse_id": warehouse_id,
            "is_active": True
        }
        }
        res = await client.put(app.url_path_for("raw_material:update-raw-material-by-id", id=raw_material_id), json=raw_material_update)
        assert res.status_code != status.HTTP_200_OK
        
class TestRawMaterialDeleteRoutes:
    async def test_raw_material_delete_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("raw_material:delete-raw-material-by-id", id="123e4567-e89b-12d3-a456-426614174000"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestRawMaterialDeleteById:
    async def test_raw_material_delete_by_id_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        
        #Create a warehouse
        warehouse = await client.post(app.url_path_for("warehouse:create-warehouse"), json={"warehouse": {"type": "test"}})
        warehouse_list_response = await client.get(app.url_path_for("warehouse:warehouse_list"))
        warehouse_list = warehouse_list_response.json().get("data")[0]
        warehouse_id = warehouse_list.get("id")        
        
        #Create a raw material
        raw_material = await client.post(app.url_path_for("raw_material:create-raw-material"), json={"raw_material": {"name": "string2","code": "string2","available_quantity": 20,"warehouse_id": warehouse_id}})
        raw_material_list_response = await client.get(app.url_path_for("raw_material:raw_material_list"))
        raw_material_list = raw_material_list_response.json().get("data")[0]
        raw_material_id = raw_material_list.get("id")
        
        raw_material = await client.get(app.url_path_for("raw_material:get-raw-material-by-id", id=raw_material_id))
        
        # Delete the raw material
        res = await client.delete(app.url_path_for("raw_material:delete-raw-material-by-id", id=raw_material_id))
        assert res.status_code == status.HTTP_200_OK
