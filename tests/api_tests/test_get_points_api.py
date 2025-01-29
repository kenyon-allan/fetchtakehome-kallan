"""Tests the get points api."""

from http import HTTPStatus
from typing import Self
from unittest.mock import patch

from flask.testing import FlaskClient
from exceptions import NoReceiptFoundException
from receipt_service import ReceiptData
from tests.api_tests.conftest import STANDARD_RECEIPT_1, STANDARD_RECEIPT_2


def fake__get_receipt(self: Self, id: str) -> ReceiptData:
    """Fake method to return a standard receipt."""
    if id == "1":
        return STANDARD_RECEIPT_1
    if id == "2":
        return STANDARD_RECEIPT_2
    raise NoReceiptFoundException(id)


@patch("receipt_service.ReceiptTracker._get_receipt", fake__get_receipt)
class TestGetPointsAPI:
    """Tests the get points api."""

    api_path_1 = "/receipts/1/points"
    api_path_2 = "/receipts/2/points"

    def test_get_points_standard_request(self: Self, client: FlaskClient) -> None:
        """Tests a standard request to the get points endpoint."""

        response = client.get(
            self.api_path_1,
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json == {"points": 28}

    def test_get_points_standard_request_2(self: Self, client: FlaskClient) -> None:
        """Tests a standard request to the get points endpoint."""

        response = client.get(
            self.api_path_2,
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json == {"points": 109}

    def test_get_points_invalid_id(self: Self, client: FlaskClient) -> None:
        """Tests an invalid request to the get points endpoint."""

        response = client.get(
            "/receipts/3/points",
        )

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json == {"message": "No receipt found for that ID."}
