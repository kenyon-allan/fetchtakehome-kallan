"""Defines API resources."""

from http import HTTPStatus
from typing import Self
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app import api
from schema import ReceiptSchema, OutputIDSchema, OutputPointsSchema, InputIDSchema

receipts_blp = Blueprint(
    name="receipts",
    import_name="receipts",
    url_prefix="/receipts",
    description="Operations on receipts",
)


@receipts_blp.route("/process")
class ReceiptProcessResource(MethodView):
    """Defines the process post endpoint."""

    @receipts_blp.doc(
        summary="Submits a receipt for processing.",
        description="Submits a receipt for processing.",
    )
    @receipts_blp.arguments(schema=ReceiptSchema, location="json")
    @receipts_blp.response(status_code=HTTPStatus.OK, schema=OutputIDSchema)
    def post(self: Self, receipt: dict) -> dict:
        """Submits a receipt for processing."""
        pass
        # 400 error response handled in app.py


@receipts_blp.route("/<string:id>/points")
class ReceiptPointsGetResource(MethodView):
    """Defines the points get endpoint."""

    @receipts_blp.doc(
        summary="Returns the points awarded for the receipt.",
        description="Returns the points awarded for the receipt.",
    )
    @receipts_blp.arguments(schema=InputIDSchema, location="path")
    @receipts_blp.response(status_code=HTTPStatus.OK, schema=OutputPointsSchema)
    def get(self: Self, id: str) -> dict:
        """Returns the points awarded for the receipt."""
        pass
        abort(http_status_code=HTTPStatus.NOT_FOUND, message="No receipt found for that ID.")


api.register_blueprint(receipts_blp)
