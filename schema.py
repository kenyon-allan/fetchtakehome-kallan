"""Defines input and output schemas to API endpoints used in the app."""

import marshmallow as ma
from marshmallow import validate


class ReceiptSchema(ma.Schema):
    """API Input schema for a receipt."""

    class ItemSchema(ma.Schema):
        """Sub-schema object for an item on a receipt."""

        short_description = ma.fields.String(
            required=True,
            validate=validate.Regexp(r"^[\w\s\-]+$"),
            metadata={
                "description": "The Short Product Description for the item.",
                "example": "Mountain Dew 12PK",
            },
        )

        price = ma.fields.Decimal(
            required=True,
            validate=validate.Range(min=0),
            places=2,
            metadata={
                "description": "The total price payed for this item.",
                "example": "6.49",
            },
        )

    retailer = ma.fields.String(
        required=True,
        validate=validate.Regexp(r"^[\w\s\-&]+$"),
        metadata={
            "description": "The name of the retailer or store the receipt is from.",
            "example": "M&M Corner Market",
        },
    )

    purchase_date = ma.fields.Date(
        required=True,
        format="%Y-%m-%d",
        metadata={
            "description": "The date of the purchase printed on the receipt.",
            "example": "2022-01-01",
        },
    )

    purchase_time = ma.fields.Time(
        required=True,
        format="%H:%M",
        metadata={
            "description": "The time of the purchase printed on the receipt. 24-hour time expected.",
            "example": "13:01",
        },
    )

    items = ma.fields.List(
        ma.fields.Nested(ItemSchema),
        required=True,
        validate=validate.Length(min=1),
    )

    total = ma.fields.Decimal(
        required=True,
        validate=validate.Range(min=0),
        places=2,
        metadata={
            "description": "The total amount paid on the receipt.",
            "example": "6.49",
        },
    )


class OutputIDSchema(ma.Schema):
    """API Output schema for a receipt ID."""

    id = ma.fields.String(
        validate=validate.Regexp(r"^\S+$"),
        metadata={
            "example": "adb6b560-0eef-42bc-9d16-df48f30e89b2",
        },
    )


class InputIDSchema(ma.Schema):
    """API Input schema for a receipt ID."""

    id = ma.fields.String(
        required=True,
        validate=validate.Regexp(r"^\S+$"),
        metadata={
            "description": "The ID of the receipt.",
        },
    )


class OutputPointsSchema(ma.Schema):
    """API Output schema for points."""

    points = ma.fields.Integer(
        required=True,
        metadata={
            "example": "100",
        },
    )
