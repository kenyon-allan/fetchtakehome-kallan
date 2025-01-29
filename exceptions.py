"""Defines custom exceptions for the project."""


class NoReceiptFoundException(Exception):
    """Exception raised when a receipt is not found in the tracker."""

    def __init__(self, receipt_id: str):
        self.receipt_id = receipt_id
        super().__init__(f"No receipt found for ID: {receipt_id}")
