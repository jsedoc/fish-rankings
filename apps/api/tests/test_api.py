import pytest

@pytest.mark.asyncio
async def test_read_main(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Food Safety Platform API"
    assert "version" in data
    assert "docs" in data

@pytest.mark.asyncio
async def test_health_check(async_client):
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_search_salmon(async_client):
    response = await async_client.get("/api/v1/search?q=Salmon")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] > 0
    # Check if Wild Salmon is in results
    found = any(f["name"] == "Wild Salmon" for f in data["foods"])
    assert found

@pytest.mark.asyncio
async def test_get_food_detail_slug(async_client):
    # Depending on seed data, 'wild-salmon' should exist
    response = await async_client.get("/api/v1/foods/slug/wild-salmon")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Wild Salmon"
    assert "contaminant_levels" in data
    assert "nutrients" in data

@pytest.mark.asyncio
async def test_get_categories(async_client):
    response = await async_client.get("/api/v1/categories")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    slugs = [c["slug"] for c in data]
    assert "seafood" in slugs
    assert "produce" in slugs
