import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_detailed_health(client: AsyncClient):
    response = await client.get("/api/v1/health/detailed")
    assert response.status_code == 200
    assert "database" in response.json()
    assert "redis" in response.json()

@pytest.mark.asyncio
async def test_plans_list(client: AsyncClient):
    response = await client.get("/api/v1/billing/plans")
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0]["name"] == "Free"
