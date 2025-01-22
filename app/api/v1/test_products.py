from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from main import app


@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_user():
    return "test_user"

@pytest.fixture
def mock_db():
    mock_session = AsyncMock(spec=AsyncSession)
    return mock_session

app.dependency_overrides[get_current_user] = lambda: "test_user"


@patch("app.api.v1.products.fetch_product_data", new_callable=AsyncMock)
@patch("app.db.database.get_db")
async def test_create_product(mock_get_db, mock_fetch_product_data, client, mock_db):
    """Тест эндпоинта POST /products"""
    mock_get_db.return_value = mock_db

    product_data = {
        "artikul": "12345",
        "name": "Test Product",
        "price": 100.0,
        "rating": 5.0,
        "stock": 10,
    }

    mock_fetch_product_data.return_value = product_data

    response = client.post("/api/v1/products", json={"artikul": "12345"})

    assert response.status_code == 200
    assert response.json() == product_data

    mock_fetch_product_data.assert_awaited_once_with("12345")
    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once()


@patch("app.tasks.scheduler.schedule_product_update")
@patch("app.db.database.get_db")
def test_subscribe_to_product(mock_get_db, mock_schedule_product_update, client, mock_db):
    """Тест эндпоинта GET /subscribe/{artikul}"""
    mock_get_db.return_value = mock_db

    response = client.get("/api/v1/products/subscribe/12345")

    assert response.status_code == 200
    assert response.json() == {"message": "Subscribed to updates for product 12345"}

    mock_schedule_product_update.assert_called_once_with("12345")
