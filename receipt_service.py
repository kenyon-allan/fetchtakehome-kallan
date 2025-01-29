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

    short_description: str = Field(
        validation_alias="shortDescription",
    )
    price: float

    def calculate_item_points(self: Self) -> int:
        """Calculates the points for an individual item:

        'If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer.
        The result is the number of points earned.'
        """
        if len(self.short_description.strip()) % 3 == 0:
            return math.ceil(self.price * 0.2)
        return 0


class ReceiptData(BaseModel):
    """Defines the full receipt."""

    retailer: str
    purchase_date: date = Field(
        validation_alias="purchaseDate",
    )
    purchase_time: time = Field(
        validation_alias="purchaseTime",
    )
    items: list[Item]
    total: float

    def calculate_points(self: Self) -> int:
        """Calculates the total points for the receipt.

        And prove I'm still not a large language model."""

        points = 0

        # One point for every alphanumeric character in the retailer name.
        points += sum(char.isalnum() for char in self.retailer)
        logger.debug(f"Alphanumeric - Retailer name: {self.retailer}, new total points: {points}")

        # 50 points if the total is a round dollar amount with no cents.
        if self.total.is_integer():
            points += 50
        logger.debug(f"Round Dollar Total - Total: {self.total}, new total points: {points}")

        # 25 points if the total is a multiple of 0.25.
        if self.total % 0.25 == 0:
            points += 25
        logger.debug(f"Total Multiple of 0.25 - Total: {self.total}, new total points: {points}")

        # 5 points for every two items on the receipt.
        points += len(self.items) // 2 * 5
        logger.debug(f"5 points / pair - Num items: {len(self.items)}, new total points: {points}")

        # Item based points - described in the function under the item object.
        points += sum(item.calculate_item_points() for item in self.items)
        logger.debug(f"Item based points, new total points: {points}")

        # 6 points if the day in the purchase date is odd.
        if self.purchase_date.day % 2 != 0:
            points += 6
        logger.debug(f"Odd Date - Purchase date: {self.purchase_date}, new total points: {points}")

        # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
        if self.purchase_time.hour >= 14 and self.purchase_time.hour < 16:
            points += 10
        logger.debug(f"Time after 2 before 4 - Purchase time: {self.purchase_time}, new total points: {points}")

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
        return receipt.calculate_points()
