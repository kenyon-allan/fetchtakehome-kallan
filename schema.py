import marshmallow as ma
from marshmallow import validate


class ReceiptSchema(ma.Schema):
    """API Input schema for a receipt."""

    reatiler = ma.fields.String(
        required=True,
        validate=validate.Regexp(r"^[\w\s\-&]+$"),
        metadata={
            "description": "The name of the retailer or store the receipt is from.",
            "example": "M&M Corner Market",
        },
    )
