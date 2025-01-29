"""Tests the process endpoint."""

from http import HTTPStatus
from typing import Self
from unittest.mock import patch

from flask.testing import FlaskClient
import pytest

from tests.api_tests.conftest import STANDARD_INPUT_BODY_1, STANDARD_INPUT_BODY_2


@patch("receipt_service.uuid.uuid4", lambda: "1")
class TestProcessAPI:
    """Tests the process API endpoint."""

    api_path = "/receipts/process"

    def test_process_standard_request(self: Self, client: FlaskClient) -> None:
        """Tests a standard request to the process endpoint."""

        response = client.post(
            self.api_path,
            json=STANDARD_INPUT_BODY_1,
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json == {"id": "1"}

    def test_process_standard_request_2(self: Self, client: FlaskClient) -> None:
        """Tests a standard request to the process endpoint."""

        response = client.post(
            self.api_path,
            json=STANDARD_INPUT_BODY_2,
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json == {"id": "1"}

    @pytest.mark.parametrize("field_name", ["retailer", "purchaseDate", "purchaseTime", "items", "total"])
    def test_process_missing_fields(
        self: Self,
        client: FlaskClient,
        field_name: str,
    ) -> None:
        """Tests an invalid request to the process endpoint."""

        input_body = STANDARD_INPUT_BODY_1.copy()

        del input_body[field_name]

        response = client.post(
            self.api_path,
            json=input_body,
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json == {"message": "The receipt is invalid."}

    @pytest.mark.parametrize("field_name", ["retailer", "purchaseDate", "purchaseTime", "items", "total"])
    def test_process_invalid_fields(
        self: Self,
        client: FlaskClient,
        field_name: str,
    ) -> None:
        """Tests an invalid request to the process endpoint."""

        input_body = STANDARD_INPUT_BODY_1.copy()

        input_body[field_name] = None

        response = client.post(
            self.api_path,
            json=input_body,
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json == {"message": "The receipt is invalid."}

    def test_process_item_missing_short_description(self: Self, client: FlaskClient) -> None:
        """Tests an invalid request to the process endpoint."""

        input_body = STANDARD_INPUT_BODY_1.copy()

        del input_body["items"][0]["shortDescription"]

        response = client.post(
            self.api_path,
            json=input_body,
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json == {"message": "The receipt is invalid."}

    def test_process_item_missing_price(self: Self, client: FlaskClient) -> None:
        """Tests an invalid request to the process endpoint."""

        input_body = STANDARD_INPUT_BODY_1.copy()

        del input_body["items"][0]["price"]

        response = client.post(
            self.api_path,
            json=input_body,
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json == {"message": "The receipt is invalid."}

    def test_process_item_invalid_price(self: Self, client: FlaskClient) -> None:
        """Tests an invalid request to the process endpoint."""

        input_body = STANDARD_INPUT_BODY_1.copy()

        input_body["items"][0]["price"] = 6.499

        response = client.post(
            self.api_path,
            json=input_body,
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json == {"message": "The receipt is invalid."}

    def test_process_item_invalid_short_description(self: Self, client: FlaskClient) -> None:
        """Tests an invalid request to the process endpoint."""

        input_body = STANDARD_INPUT_BODY_1.copy()

        input_body["items"][0]["shortDescription"] = "&"

        response = client.post(
            self.api_path,
            json=input_body,
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json == {"message": "The receipt is invalid."}

    def test_process_invalid_retailer(self: Self, client: FlaskClient) -> None:
        """Tests an invalid request to the process endpoint."""

        input_body = STANDARD_INPUT_BODY_1.copy()

        input_body["retailer"] = "%"

        response = client.post(
            self.api_path,
            json=input_body,
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json == {"message": "The receipt is invalid."}

    def test_process_invalid_purchase_date(self: Self, client: FlaskClient) -> None:
        """Tests an invalid request to the process endpoint."""

        input_body = STANDARD_INPUT_BODY_1.copy()

        input_body["purchaseDate"] = "01/02/2022"  # Wrong format

        response = client.post(
            self.api_path,
            json=input_body,
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json == {"message": "The receipt is invalid."}

    def test_process_invalid_purchase_time(self: Self, client: FlaskClient) -> None:
        """Tests an invalid request to the process endpoint."""

        input_body = STANDARD_INPUT_BODY_1.copy()

        input_body["purchaseTime"] = "01:02:03"  # Wrong format

        response = client.post(
            self.api_path,
            json=input_body,
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json == {"message": "The receipt is invalid."}

    def test_process_invalid_total(self: Self, client: FlaskClient) -> None:
        """Tests an invalid request to the process endpoint."""

        input_body = STANDARD_INPUT_BODY_1.copy()

        input_body["total"] = 6.499

        response = client.post(
            self.api_path,
            json=input_body,
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json == {"message": "The receipt is invalid."}

    def test_process_invalid_items_amount(self: Self, client: FlaskClient) -> None:
        """Tests an invalid request to the process endpoint."""

        input_body = STANDARD_INPUT_BODY_1.copy()

        input_body["items"] = []

        response = client.post(
            self.api_path,
            json=input_body,
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json == {"message": "The receipt is invalid."}

    def test_process_invalid_item(self: Self, client: FlaskClient) -> None:
        """Tests an invalid request to the process endpoint."""

        input_body = STANDARD_INPUT_BODY_1.copy()

        input_body["items"][0] = {}

        response = client.post(
            self.api_path,
            json=input_body,
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json == {"message": "The receipt is invalid."}
