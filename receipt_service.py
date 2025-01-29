"""Defines the logic behind points calculation for a receipt."""

from typing import Self
from pydantic import BaseModel, Field
from datetime import time, date

from exceptions import NoReceiptFoundException


class Item(BaseModel):
    """Defines an item on the receipt."""

    short_description: str = Field(
        validation_alias="shortDescription",
    )
    price: float


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
        return 0


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
        receipt_id = ""
        self.receipt_id_to_data[receipt_id] = receipt_data
        return receipt_id

    def _get_receipt(self, receipt_id: str) -> ReceiptData:
        """Retrieves a receipt from the tracker."""
        receipt = self.receipt_id_to_data.get(receipt_id, None)
        if receipt is None:
            raise NoReceiptFoundException(receipt_id)
        return receipt

    def get_points_for_receipt(self, receipt_id: str) -> int:
        """Returns the points awarded for a receipt."""
        # First check if we've calculated the points before to save time.
        if receipt_id in self.receipt_id_to_points:
            return self.receipt_id_to_points[receipt_id]
        receipt = self._get_receipt(receipt_id)
        return receipt.calculate_points()
