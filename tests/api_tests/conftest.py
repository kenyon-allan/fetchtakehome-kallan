"""Configures important fixtures for testing."""

from flask import Flask
import pytest

from app import create_app
from receipt_service import ReceiptData


@pytest.fixture()
def app():
    """Creates a fake testing app."""
    app = create_app()
    app.config["TESTING"] = True
    yield app


@pytest.fixture()
def client(app: Flask):
    """Creates a fake testing client."""
    with app.test_client() as client:
        yield client


STANDARD_INPUT_BODY_1 = {
    "retailer": "Target",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
        {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
        {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
        {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
        {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
        {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00"},
    ],
    "total": "35.35",
}
STANDARD_INPUT_BODY_2 = {
    "retailer": "M&M Corner Market",
    "purchaseDate": "2022-03-20",
    "purchaseTime": "14:33",
    "items": [
        {"shortDescription": "Gatorade", "price": "2.25"},
        {"shortDescription": "Gatorade", "price": "2.25"},
        {"shortDescription": "Gatorade", "price": "2.25"},
        {"shortDescription": "Gatorade", "price": "2.25"},
    ],
    "total": "9.00",
}
STANDARD_RECEIPT_1 = ReceiptData(**STANDARD_INPUT_BODY_1)
STANDARD_RECEIPT_2 = ReceiptData(**STANDARD_INPUT_BODY_2)
