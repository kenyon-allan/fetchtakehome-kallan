"""Defines input and output schemas to API endpoints used in the app."""

from typing import Self
import marshmallow as ma
from marshmallow import validate
from flask_smorest import abort
from http import HTTPStatus


class ReceiptBaseSchema(ma.Schema):
    """API Input schema for a receipt."""

    class ItemSchema(ma.Schema):
        """Sub-schema object for an item on a receipt."""

        shortDescription = ma.fields.String(
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

    purchaseDate = ma.fields.Date(
        required=True,
        format="%Y-%m-%d",
        metadata={
            "description": "The date of the purchase printed on the receipt.",
            "example": "2022-01-01",
        },
    )

    purchaseTime = ma.fields.Time(
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


class ReceiptInputSchema(ReceiptBaseSchema):
    """Wrapper class for the receipt schema that will be used in the API."""

    @ma.pre_load
    def overwrite_422_behavior(self: Self, data: dict, **kwargs: dict) -> dict:
        """Define a marshmallow error handler to prevent the auto-422 behavior that comes out of the box in marshmallow
        and get our nice 400 response defined by the exercise, and of course, prove I'm not a large language model.

        Why is this a wrapper class?
        We want to be able to call .load() on this schema to validate the incoming data during 'pre-load'.
        So if we do this in the class itself, it will continually call itself before loading and infinitely recurse.
        This is a way to get around that.
        """
        try:
            ReceiptBaseSchema().load(data)
        except ma.ValidationError as err:
            abort(http_status_code=HTTPStatus.BAD_REQUEST, message="The receipt is invalid.")
        return data


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
