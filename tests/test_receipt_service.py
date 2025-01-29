"""Tests the receipt_service"""

from typing import Self
from unittest.mock import patch
from exceptions import NoReceiptFoundException
from receipt_service import Item, ReceiptData, ReceiptTracker
from datetime import date, time
import pytest


class TestItem:
    """Tests the Item class."""

    def test_calculate_item_points_multiple_of_3(self: Self) -> None:
        """Tests a standard case where an item has a description which is a multiple of 3."""
        item = Item(shortDescription="abc", price=10.00)
        assert item.calculate_item_points() == 2

    def test_calculate_item_points_ceiling_multiple_of_3(self: Self) -> None:
        """Tests a case where an item has a description which is a multiple of 3 and the price * 0.2 is not a whole number."""
        item = Item(shortDescription="abc", price=1.00)
        assert item.calculate_item_points() == 1  # 1 * 0.2 = 0.2, rounded up to 1

    def test_calculate_item_points_non_multiple_of_3(self: Self) -> None:
        """Tests a case where an item has a description which is not a multiple of 3."""
        item = Item(shortDescription="abcd", price=10.00)
        assert item.calculate_item_points() == 0


class TestReceiptData:
    """Tests the ReceiptData class."""

    @pytest.mark.parametrize("retailer, expected_value", [("aaa111* ", 6), ("   ", 0)])
    def test_calculate_alphanumeric_points(self: Self, retailer: str, expected_value: int) -> None:
        """Tests the alphanumeric points calculation method."""
        receipt = ReceiptData(
            retailer=retailer,
            purchaseDate=date(2025, 1, 1),
            purchaseTime=time(0, 0, 0),
            items=[Item(shortDescription="abc", price=10.00)],
            total=1.00,
        )
        assert receipt._calculate_alphanumeric_points() == expected_value

    @pytest.mark.parametrize("total, expected_value", [(1.00, 50), (1.01, 0)])
    def test_calculate_round_dollar_total_points(self: Self, total: float, expected_value: int) -> None:
        """Tests the round dollar total points calculation method."""
        receipt = ReceiptData(
            retailer="aaa",
            purchaseDate=date(2025, 1, 1),
            purchaseTime=time(0, 0, 0),
            items=[Item(shortDescription="abc", price=10.00)],
            total=total,
        )
        assert receipt._calculate_round_dollar_total_points() == expected_value

    @pytest.mark.parametrize("total, expected_value", [(1.00, 25), (1.01, 0)])
    def test_calculate_quarter_multiple_total_points(self: Self, total: float, expected_value: int) -> None:
        """Tests the quarter multiple total points calculation method."""
        receipt = ReceiptData(
            retailer="aaa",
            purchaseDate=date(2025, 1, 1),
            purchaseTime=time(0, 0, 0),
            items=[Item(shortDescription="abc", price=10.00)],
            total=total,
        )
        assert receipt._calculate_quarter_multiple_total_points() == expected_value

    @pytest.mark.parametrize(
        "items, expected_value",
        [
            ([Item(shortDescription="abc", price=10.00)], 0),
            ([Item(shortDescription="abc", price=10.00)] * 2, 5),
            ([Item(shortDescription="abc", price=10.00)] * 3, 5),
            ([Item(shortDescription="abc", price=10.00)] * 4, 10),
        ],
    )
    def test_calculate_item_length_points(self: Self, items: list[Item], expected_value: int) -> None:
        """Tests the item length points calculation method when there are two items."""
        receipt = ReceiptData(
            retailer="aaa",
            purchaseDate=date(2025, 1, 1),
            purchaseTime=time(0, 0, 0),
            items=items,
            total=1.00,
        )
        assert receipt._calculate_item_length_points() == expected_value

    @pytest.mark.parametrize(
        "items, expected_value",
        [
            ([Item(shortDescription="abc", price=10.00)], 2),
            ([Item(shortDescription="abcd", price=10.00)], 0),
            ([Item(shortDescription="abc", price=10.00)] * 2, 4),
        ],
    )
    def test_calculate_sub_item_points(self: Self, items: list[Item], expected_value: int) -> None:
        """Tests the sub item points calculation method."""
        receipt = ReceiptData(
            retailer="aaa",
            purchaseDate=date(2025, 1, 1),
            purchaseTime=time(0, 0, 0),
            items=items,
            total=1.00,
        )
        assert receipt._calculate_sub_item_points() == expected_value

    @pytest.mark.parametrize(
        "purchase_date, expected_value",
        [(date(2025, 1, 1), 6), (date(2025, 1, 2), 0)],
    )
    def test_calculate_purchase_day_odd_points(self: Self, purchase_date: date, expected_value: int) -> None:
        """Tests the purchase day odd points calculation method."""
        receipt = ReceiptData(
            retailer="aaa",
            purchaseDate=purchase_date,
            purchaseTime=time(0, 0, 0),
            items=[Item(shortDescription="abc", price=10.00)],
            total=1.00,
        )
        assert receipt._calculate_purchase_day_odd_points() == expected_value

    @pytest.mark.parametrize(
        "purchase_time, expected_value",
        [(time(14, 0, 0), 0), (time(13, 59, 59), 0), (time(16, 0, 0), 0), (time(15, 59, 59), 10), (time(14, 1, 0), 10)],
    )
    def test_calculate_purchase_time_points(self: Self, purchase_time: time, expected_value: int) -> None:
        """Tests the purchase time points calculation method."""
        receipt = ReceiptData(
            retailer="aaa",
            purchaseDate=date(2025, 1, 1),
            purchaseTime=purchase_time,
            items=[Item(shortDescription="abc", price=10.00)],
            total=1.00,
        )
        assert receipt._calculate_purchase_time_points() == expected_value

    def test_calculate_points_exercise_example_1(self: Self) -> None:
        """Test the example provided by the exercise."""

        receipt = ReceiptData(
            **{
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
        )

        assert receipt.calculate_points() == 28

    def test_calculate_points_exercise_example_2(self: Self) -> None:
        """Test the example provided by the exercise."""

        receipt = ReceiptData(
            **{
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
        )

        assert receipt.calculate_points() == 109


@patch("receipt_service.uuid.uuid4", lambda: "1")
@patch("receipt_service.ReceiptData.calculate_points", lambda self: 1)
class TestReceiptTracker:
    """Tests the receipttracker class."""

    @pytest.fixture(autouse=True)
    def tracker_reset(self: Self):
        """Resets the tracker between tests."""
        yield
        tracker = ReceiptTracker()
        tracker.receipt_id_to_data = {}
        tracker.receipt_id_to_points = {}

    def test_add_receipt(self: Self) -> None:
        """Tests the add_receipt method."""
        tracker = ReceiptTracker()
        receipt = ReceiptData(
            retailer="aaa",
            purchaseDate=date(2025, 1, 1),
            purchaseTime=time(0, 0, 0),
            items=[Item(shortDescription="abc", price=10.00)],
            total=1.00,
        )
        tracker.add_receipt(receipt)
        assert tracker.receipt_id_to_data == {"1": receipt}

    def test_get_receipt_valid(self: Self) -> None:
        """Tests the get_receipt method with a valid receipt."""
        tracker = ReceiptTracker()
        receipt = ReceiptData(
            retailer="aaa",
            purchaseDate=date(2025, 1, 1),
            purchaseTime=time(0, 0, 0),
            items=[Item(shortDescription="abc", price=10.00)],
            total=1.00,
        )
        tracker.add_receipt(receipt)
        assert tracker._get_receipt("1") == receipt

    def test_get_receipt_invalid(self: Self) -> None:
        """Tests the get_receipt method with an invalid receipt."""
        tracker = ReceiptTracker()
        with pytest.raises(NoReceiptFoundException):
            tracker._get_receipt("1")

    def test_get_points_for_receipt_valid(self: Self) -> None:
        """Tests the get_points_for_receipt method with a valid receipt."""
        tracker = ReceiptTracker()
        receipt = ReceiptData(
            retailer="aaa",
            purchaseDate=date(2025, 1, 1),
            purchaseTime=time(0, 0, 0),
            items=[Item(shortDescription="abc", price=10.00)],
            total=1.00,
        )
        tracker.add_receipt(receipt)
        assert tracker.get_points_for_receipt("1") == 1
        assert tracker.receipt_id_to_points == {"1": 1}

    def test_get_points_for_receipt_already_gotten_once(self: Self) -> None:
        """Tests the get_points_for_receipt method with a valid receipt that has already been gotten once."""
        tracker = ReceiptTracker()
        receipt = ReceiptData(
            retailer="aaa",
            purchaseDate=date(2025, 1, 1),
            purchaseTime=time(0, 0, 0),
            items=[Item(shortDescription="abc", price=10.00)],
            total=1.00,
        )
        tracker.add_receipt(receipt)
        tracker.get_points_for_receipt("1")
        tracker.get_points_for_receipt("1")  # second call should reference the cache.
