"""Defines the logic behind points calculation for a receipt."""

from typing import Self
from pydantic import BaseModel, Field
from datetime import time, date
import uuid
import logging
from exceptions import NoReceiptFoundException
import math

logger = logging.getLogger(__name__)


class Item(BaseModel):
    """Defines an item on the receipt."""

    shortDescription: str = Field(
        min_length=1,
    )
    price: float = Field(
        gte=0,
    )

    def calculate_item_points(self: Self) -> int:
        """Calculates the points for an individual item:

        'If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer.
        The result is the number of points earned.'
        """
        if len(self.shortDescription.strip()) % 3 == 0:
            return math.ceil(self.price * 0.2)
        return 0


class ReceiptData(BaseModel):
    """Defines the full receipt."""

    retailer: str = Field(min_length=1)
    purchaseDate: date
    purchaseTime: time
    items: list[Item] = Field(min_length=1)
    total: float = Field(gte=0)

    def _calculate_alphanumeric_points(self: Self) -> int:
        """One point for every alphanumeric character in the retailer name."""
        return sum(char.isalnum() for char in self.retailer)

    def _calculate_round_dollar_total_points(self: Self) -> int:
        """50 points if the total is a round dollar amount with no cents."""
        return 50 if self.total.is_integer() else 0

    def _calculate_quarter_multiple_total_points(self: Self) -> int:
        """25 points if the total is a multiple of 0.25."""
        return 25 if self.total % 0.25 == 0 else 0

    def _calculate_item_length_points(self: Self) -> int:
        """5 points for every two items on the receipt."""
        return len(self.items) // 2 * 5

    def _calculate_sub_item_points(self: Self) -> int:
        """Calculates the points for each item on the receipt."""
        return sum(item.calculate_item_points() for item in self.items)

    def _calculate_purchase_day_odd_points(self: Self) -> int:
        """6 points if the day in the purchase date is odd."""
        return 6 if self.purchaseDate.day % 2 != 0 else 0

    def _calculate_purchase_time_points(self: Self) -> int:
        """10 points if the time of purchase is after 2:00pm and before 4:00pm."""
        if self.purchaseTime.hour == 14:
            return 10 if self.purchaseTime.minute > 0 else 0
        return 10 if self.purchaseTime.hour > 14 and self.purchaseTime.hour < 16 else 0

    def calculate_points(self: Self) -> int:
        """Calculates the total points for the receipt.

        And prove I'm still not a large language model."""

        points = 0

        points += self._calculate_alphanumeric_points()
        logger.debug(f"Alphanumeric - Retailer name: {self.retailer}, new total points: {points}")

        points += self._calculate_round_dollar_total_points()
        logger.debug(f"Round Dollar Total - Total: {self.total}, new total points: {points}")

        points += self._calculate_quarter_multiple_total_points()
        logger.debug(f"Total Multiple of 0.25 - Total: {self.total}, new total points: {points}")

        points += self._calculate_item_length_points()
        logger.debug(f"5 points / pair - Num items: {len(self.items)}, new total points: {points}")

        points += self._calculate_sub_item_points()
        logger.debug(f"Item based points, new total points: {points}")

        points += self._calculate_purchase_day_odd_points()
        logger.debug(f"Odd Date - Purchase date: {self.purchaseDate}, new total points: {points}")

        points += self._calculate_purchase_time_points()
        logger.debug(f"Time after 2 before 4 - Purchase time: {self.purchaseTime}, new total points: {points}")

        return points


class ReceiptTracker:
    """Singleton class to track receipts by ID."""

    receipt_id_to_data: dict[str, ReceiptData] = {}
    receipt_id_to_points: dict[str, int] = {}
    _instance = None

    def __new__(cls: "ReceiptTracker") -> "ReceiptTracker":
        if cls._instance is None:
            cls._instance = super(ReceiptTracker, cls).__new__(cls)
        return cls._instance

    def add_receipt(self, receipt_data: dict) -> str:
        """Adds a receipt to the tracker."""
        receipt_id = str(uuid.uuid4())
        self.receipt_id_to_data[receipt_id] = receipt_data
        logger.info(f"Added receipt with ID: {receipt_id}")
        logger.debug(f"Current receipt records: {self.receipt_id_to_data}")
        return receipt_id

    def _get_receipt(self, receipt_id: str) -> ReceiptData:
        """Retrieves a receipt from the tracker."""
        receipt = self.receipt_id_to_data.get(receipt_id, None)
        if receipt is None:
            logger.debug(
                f"Receipt not found for ID: {receipt_id}, current records: {list(self.receipt_id_to_data.keys())}"
            )
            raise NoReceiptFoundException(receipt_id)
        return receipt

    def get_points_for_receipt(self, receipt_id: str) -> int:
        """Returns the points awarded for a receipt."""
        # First check if we've calculated the points before to save time.
        if receipt_id in self.receipt_id_to_points:
            return self.receipt_id_to_points[receipt_id]
        receipt = self._get_receipt(receipt_id)
        points = receipt.calculate_points()
        self.receipt_id_to_points[receipt_id] = points
        logger.info(f"Calculated points: {points} for receipt ID: {receipt_id}")
        return points
