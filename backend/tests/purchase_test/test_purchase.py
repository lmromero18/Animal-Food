import uuid
import pytest

from fastapi import FastAPI, status
from loguru import logger
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

class TestPurchaseCreateRoutes:
    async def test_create_purchase_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.post(app.url_path_for("purchase:create-purchase"), json={})
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestPurchaseCreate:
    async def test_create_product_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client

        supplier_json = {
            "supplier": {
                "name": "string",
                "address": "string"
            }
        }

        supplier = await client.post(app.url_path_for("supplier:create-supplier"), json=supplier_json)
        assert supplier.status_code == status.HTTP_201_CREATED
        supplier_list_response = await client.get(app.url_path_for("supplier:supplier_list"))
        supplier_list = supplier_list_response.json().get("data")[0]
        supplier_id = supplier_list.get("id")

        warehouse = await client.post(app.url_path_for("warehouse:create-warehouse"), json={"warehouse": {"type": "test"}})
        warehouse_list_response = await client.get(app.url_path_for("warehouse:warehouse_list"))
        warehouse_list = warehouse_list_response.json().get("data")[0]
        warehouse_id = warehouse_list.get("id")

        raw_material = await client.post(app.url_path_for("raw_material:create-raw-material"), json={"raw_material": {"name": "string","code": "string","available_quantity": 20,"warehouse_id": warehouse_id}})
        assert raw_material.status_code == status.HTTP_201_CREATED
        raw_material_list_response = await client.get(app.url_path_for("raw_material:raw_material_list"))
        raw_material_list = raw_material_list_response.json().get("data")[0]
        raw_material_id = raw_material_list.get("id")

        json_purchase = {
            "purchase": {
                "supplier_id": supplier_id,
                "raw_material_id": raw_material_id,
                "quantity": 20
            }
        }

        res = await client.post(app.url_path_for("purchase:create-purchase"), json=json_purchase)
        assert res.status_code == status.HTTP_201_CREATED
        
        
class TestPurchaseGetByListRoutes:
    async def test_purchase_list_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("purchase:purchase_list"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestPurchaseList:
    async def test_purchase_list_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        res = await client.get(app.url_path_for("purchase:purchase_list"))
        assert res.status_code == status.HTTP_200_OK
        
class TestPurchaseGetRoutes:
    async def test_purchase_by_id_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("purchase:get-purchase-by-id", id="123e4567-e89b-12d3-a456-426614174000"))
        assert res.status_code != status.HTTP_404_NOT_FOUND




class TestPurchaseGetById:
    async def test_purchase_by_id_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client

        supplier_json = {
            "supplier": {
                "name": "string",
                "address": "string"
            }
        }

        supplier_list_response = await client.get(app.url_path_for("supplier:supplier_list"))
        supplier_list = supplier_list_response.json().get("data")[0]
        supplier_id = supplier_list.get("id")

        warehouse = await client.post(app.url_path_for("warehouse:create-warehouse"), json={"warehouse": {"type": "test"}})
        warehouse_list_response = await client.get(app.url_path_for("warehouse:warehouse_list"))
        warehouse_list = warehouse_list_response.json().get("data")[0]
        warehouse_id = warehouse_list.get("id")

        raw_material_list_response = await client.get(app.url_path_for("raw_material:raw_material_list"))
        raw_material_list = raw_material_list_response.json().get("data")[0]
        raw_material_id = raw_material_list.get("id")

        json_purchase = {
            "purchase": {
                "supplier_id": supplier_id,
                "raw_material_id": raw_material_id,
                "quantity": 20
            }
        }

        purchase = await client.post(app.url_path_for("purchase:create-purchase"), json=json_purchase)
        assert purchase.status_code == status.HTTP_201_CREATED
        purchase_list_response = await client.get(app.url_path_for("purchase:purchase_list"))
        purchase_list = purchase_list_response.json().get("data")[0]
        purchase_id = purchase_list.get("id")

        res = await client.get(app.url_path_for("purchase:get-purchase-by-id", id=purchase_id))
        assert res.status_code == status.HTTP_200_OK
        
class TestPurchaseUpdateRoutes:
    async def test_purchase_update_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.get(app.url_path_for("purchase:update-purchase-by-id", id="123e4567-e89b-12d3-a456-426614174000"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
        
class TestPurchaseUpdateById:
    async def test_purchase_update_by_id_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        
        supplier_json = {
            "supplier": {
                "name": "string",
                "address": "string"
            }
        }
        
        supplier_list_response = await client.get(app.url_path_for("supplier:supplier_list"))
        supplier_list = supplier_list_response.json().get("data")[0]
        supplier_id = supplier_list.get("id")
        
        warehouse = await client.post(app.url_path_for("warehouse:create-warehouse"), json={"warehouse": {"type": "test"}})
        warehouse_list_response = await client.get(app.url_path_for("warehouse:warehouse_list"))
        warehouse_list = warehouse_list_response.json().get("data")[0]
        warehouse_id = warehouse_list.get("id")
        
        raw_material_list_response = await client.get(app.url_path_for("raw_material:raw_material_list"))
        raw_material_list = raw_material_list_response.json().get("data")[0]
        raw_material_id = raw_material_list.get("id")        
        
        json_purchase = {
            "purchase": {
                "supplier_id": supplier_id,
                "raw_material_id": raw_material_id,
                "quantity": 20
            }
        }
        
        purchase = await client.post(app.url_path_for("purchase:create-purchase"), json=json_purchase)
        assert purchase.status_code == status.HTTP_201_CREATED
        purchase_list_response = await client.get(app.url_path_for("purchase:purchase_list"))
        purchase_list = purchase_list_response.json().get("data")[0]
        purchase_id = purchase_list.get("id")
        
        supplier_update_json = {
            "purchase_update": {
                "supplier_id": supplier_id,
                "raw_material_id": raw_material_id,
                "quantity": 2,
                "is_delivered": True
            }
        }
        res = await client.put(app.url_path_for("purchase:update-purchase-by-id", id=purchase_id), json=supplier_update_json)
        assert res.status_code == status.HTTP_200_OK
        
class TestPurchaseDeleteRoutes:
    async def test_price_delete_route_exists(self, app: FastAPI, client:AsyncClient) -> None:
        res = await client.delete(app.url_path_for("purchase:delete-purchase-by-id", id="123e4567-e89b-12d3-a456-426614174000"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
class TestPurchaseDeleteById:
    async def test_purchase_delete_by_id_route(self, authorized_client: AsyncClient, app:FastAPI) -> None:
        client = await authorized_client
        purchase_list_response = await client.get(app.url_path_for("purchase:purchase_list"))
        purchase_list = purchase_list_response.json().get("data")[0]
        purchase_id = purchase_list.get("id")
        
        res = await client.delete(app.url_path_for("purchase:delete-purchase-by-id", id=purchase_id))
        assert res.status_code == status.HTTP_200_OK       
