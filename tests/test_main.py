"""Tests for FastapiServiceOrderservice API."""
import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.mark.anyio
async def test_root():
    """Test root endpoint returns service info."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "fastapi-service-orderservice"
    assert "message" in data


@pytest.mark.anyio
async def test_health_check():
    """Test health check endpoint."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "fastapi-service-orderservice"
    assert "timestamp" in data
    assert "version" in data


@pytest.mark.anyio
async def test_readiness_check():
    """Test readiness check endpoint."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/ready")
    
    assert response.status_code == 200
    data = response.json()
    assert "ready" in data
    assert "checks" in data


@pytest.mark.anyio
async def test_list_items_empty():
    """Test listing items when empty."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/items")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.anyio
async def test_create_and_get_item():
    """Test creating and retrieving an item."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Create item
        item_data = {"id": 1, "name": "Test Item", "description": "A test item"}
        response = await client.post("/api/items", json=item_data)
        assert response.status_code == 200
        
        # Get item
        response = await client.get("/api/items/1")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Item"


@pytest.mark.anyio
async def test_get_item_not_found():
    """Test getting non-existent item returns 404."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/items/9999")
    
    assert response.status_code == 404
