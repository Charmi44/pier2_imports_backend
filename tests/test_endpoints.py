import os
import sys

# Adding the project root directory to sys.path so that 'app' can be imported when running tests directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

# Create a FastAPI test client to simulate HTTP requests
client = TestClient(app)


# Mocking the `crud.get_order_history` function to return fake order data
@patch("app.crud.get_order_history")
def test_get_order_history(mock_get_order_history):
    # Define mocked return value
    mock_get_order_history.return_value = [
        {
            "order_id": 1,
            "timestamp": "2025-06-17T15:00:00",
            "in_store": True,
            "billing_address": {},
            "items": []
        }
    ]

    # Call the API
    response = client.get("/customer/johndoe@gmail.com/orders")

    # Assertions
    assert response.status_code == 200
    assert len(response.json()) == 1


# Mocks total count of orders grouped by billing zip code
@patch("app.crud.get_orders_grouped_by_billing_zip")
def test_orders_by_billing_zip(mock_func):
    mock_func.return_value = [{"zip_code": "12345", "order_count": 3}]
    response = client.get("/analytics/orders_by_billing_zip")
    assert response.status_code == 200
    assert response.json()[0]["zip_code"] == "12345"


# Mocks total count of orders grouped by shipping zip code
@patch("app.crud.get_orders_grouped_by_shipping_zip")
def test_orders_by_shipping_zip(mock_func):
    mock_func.return_value = [{"zip_code": "54321", "order_count": 5}]
    response = client.get("/analytics/orders_by_shipping_zip")
    assert response.status_code == 200
    assert response.json()[0]["order_count"] == 5


# Mocks response for peak in-store purchase hour
@patch("app.crud.get_peak_instore_purchase_hour")
def test_in_store_peak_hour(mock_func):
    mock_func.return_value = {"3pm": 12}
    response = client.get("/analytics/in_store_peak_hour")
    assert response.status_code == 200
    assert "3pm" in response.json()


# Mocks response to return top customers who made the most in-store purchases
@patch("app.crud.get_top_instore_customer")
def test_top_instore_customer(mock_func):
    mock_func.return_value = [
        {
            "email": "x@gmail.com",
            "first_name": "X",
            "last_name": "Y",
            "phone": "123",
            "in_store_count": 5
        }
    ]
    response = client.get("/analytics/top_instore_customers")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["in_store_count"] == 5
