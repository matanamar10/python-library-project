# tests/test_routes.py

import pytest
from httpx import AsyncClient
from src.app import create_app

app = create_app(library_name="TestLibrary")


@pytest.mark.asyncio
async def test_add_library_item():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/library/items",
            json={"library_items": [{"title": "Test Book", "isbn": "123456789", "is_borrowed": False}]}
        )
        assert response.status_code == 200
        assert response.json() == {"message": "The new items successfully added"}


@pytest.mark.asyncio
async def test_add_patron():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/library/patrons",
            json={"patrons_to_add": [{"name": "John Doe", "patron_id": "123456789", "patron_items": {}}]}
        )
        assert response.status_code == 200
        assert response.json() == {"message": "The new patrons successfully added"}


@pytest.mark.asyncio
async def test_delete_patron():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First, ensure the patron is added
        await client.post(
            "/library/patrons",
            json={"patrons_to_add": [{"name": "John Doe", "patron_id": "123456789", "patron_items": {}}]}
        )
        # Then delete the patron
        response = await client.delete("/library/patrons/123456789")
        assert response.status_code == 200
        assert response.json() == {"message": "Patron successfully removed"}


@pytest.mark.asyncio
async def test_delete_item():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First, ensure the item is added
        await client.post(
            "/library/items",
            json={"library_items": [{"title": "Test Book", "isbn": "123456789", "is_borrowed": False}]}
        )
        # Then delete the item
        response = await client.delete("/library/items/123456789")
        assert response.status_code == 200
        assert response.json() == {"message": "Item successfully removed from the library"}


@pytest.mark.asyncio
async def test_get_library_item():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First, ensure the item is added
        await client.post(
            "/library/items",
            json={"library_items": [{"title": "Test Book", "isbn": "123456789", "is_borrowed": False}]}
        )
        # Then get the item
        response = await client.get("/library/items/123456789")
        assert response.status_code == 200
        assert response.json() == {"isbn": "123456789", "title": "Test Book", "is_borrowed": False}


@pytest.mark.asyncio
async def test_get_library_patron():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First, ensure the patron is added
        await client.post(
            "/library/patrons",
            json={"patrons_to_add": [{"name": "John Doe", "patron_id": "123456789", "patron_items": {}}]}
        )
        # Then get the patron
        response = await client.get("/library/patrons/123456789")
        assert response.status_code == 200
        assert response.json() == {"name": "John Doe", "patron_id": "123456789", "patron_items": {}}


@pytest.mark.asyncio
async def test_borrow_item():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First, ensure the item and patron are set up
        await client.post(
            "/library/items",
            json={"library_items": [{"title": "Test Book", "isbn": "123456789", "is_borrowed": False}]}
        )
        await client.post(
            "/library/patrons",
            json={"patrons_to_add": [{"name": "John Doe", "patron_id": "123456789", "patron_items": {}}]}
        )
        # Then borrow the item
        response = await client.patch(
            "/borrowing/borrow",
            json={"library_item": {"isbn": "123456789"}, "patron_id": "123456789"}
        )
        assert response.status_code == 200
        assert response.json() == {"message": "Item successfully borrowed"}


@pytest.mark.asyncio
async def test_return_item():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First, ensure the item and patron are set up
        await client.post(
            "/library/items",
            json={"library_items": [{"title": "Test Book", "isbn": "123456789", "is_borrowed": True}]}
        )
        await client.post(
            "/library/patrons",
            json={"patrons_to_add": [
                {"name": "John Doe", "patron_id": "123456789", "patron_items": {"123456789": "2024-01-01T00:00:00"}}]}
        )
        # Then return the item
        response = await client.patch(
            "/borrowing/return",
            json={"library_item": {"isbn": "123456789"}, "patron_id": "123456789"}
        )
        assert response.status_code == 200
        assert response.json() == {"message": "Item successfully returned"}


@pytest.mark.asyncio
async def test_item_already_exists_error():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First, add an item to simulate existence
        await client.post(
            "/library/items",
            json={"library_items": [{"title": "Test Book", "isbn": "123456789", "is_borrowed": False}]}
        )
        # Then attempt to add the same item again to trigger an error
        response = await client.post(
            "/library/items",
            json={"library_items": [{"title": "Test Book", "isbn": "123456789", "is_borrowed": False}]}
        )
        assert response.status_code == 400
        assert response.json() == {
            "detail": "The library item with isbn 123456789 is already exist in the library system"}


@pytest.mark.asyncio
async def test_patron_already_exists_error():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First, add a patron to simulate existence
        await client.post(
            "/library/patrons",
            json={"patrons_to_add": [{"name": "John Doe", "patron_id": "123456789", "patron_items": {}}]}
        )
        # Then attempt to add the same patron again to trigger an error
        response = await client.post(
            "/library/patrons",
            json={"patrons_to_add": [{"name": "John Doe", "patron_id": "123456789", "patron_items": {}}]}
        )
        assert response.status_code == 400
        assert response.json() == {
            "detail": "The library patron with id 123456789 is already exist in the library system"}
