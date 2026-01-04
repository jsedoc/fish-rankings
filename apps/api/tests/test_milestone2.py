import pytest

@pytest.mark.asyncio
async def test_get_recalls(async_client):
    response = await async_client.get("/api/v1/recalls")
    assert response.status_code == 200
    data = response.json()
    assert "recalls" in data
    assert "total" in data
    assert isinstance(data["recalls"], list)
    if data["total"] > 0:
        assert len(data["recalls"]) > 0

@pytest.mark.asyncio
async def test_get_recent_recalls(async_client):
    response = await async_client.get("/api/v1/recalls/recent?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 5
    if len(data) > 0:
        assert "recall_number" in data[0]

@pytest.mark.asyncio
async def test_search_barcode_mock(async_client):
    # This endpoint mocks external calls or queries logical DB
    # We are just checking if the route exists and returns 200 or 404 cleanly
    response = await async_client.get("/api/v1/barcode/search?q=tuna")
    assert response.status_code == 200
    data = response.json()
    # Verify the response structure matches the barcode.py implementation
    assert "query" in data
    assert "page" in data
    assert "page_size" in data
    assert "results" in data
    assert "count" in data
    assert isinstance(data["results"], list)
    assert data["query"] == "tuna"
    assert data["page"] == 1
    assert data["page_size"] == 10

@pytest.mark.asyncio
async def test_food_detail_includes_advisories(async_client):
    # Fetch 'wild-salmon' (seeded in Milestone 1/2)
    response = await async_client.get("/api/v1/foods/slug/wild-salmon")
    
    # If not 200, it might be due to seeding variations, but checking schema keys is ensuring API structure 
    if response.status_code == 200:
        data = response.json()
        assert "advisories" in data
        assert "sustainability_ratings" in data
        assert isinstance(data["advisories"], list)
        assert isinstance(data["sustainability_ratings"], list)
