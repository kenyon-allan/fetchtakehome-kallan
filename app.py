"""Handles the set up of the app."""

from http import HTTPStatus
from flask import Flask
from typing import Self
from flask.views import MethodView
from flask_smorest import Blueprint, abort, Api
from exceptions import NoReceiptFoundException
from receipt_service import ReceiptData, ReceiptTracker
from schema import ReceiptInputSchema, OutputIDSchema, OutputPointsSchema, InputIDSchema
import logging

# Configure our logger.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """Creates the flask app."""
    app = Flask(__name__)
    config = {
        "API_TITLE": "Receipt Processor",
        "API_VERSION": "v1.0.0",
        "OPENAPI_VERSION": "3.0.3",
    }
    app.config.update(config)
    return app


api = Api(create_app())


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
    @receipts_blp.arguments(schema=ReceiptInputSchema, location="json")
    @receipts_blp.response(status_code=HTTPStatus.OK, schema=OutputIDSchema)
    def post(self: Self, receipt: dict) -> dict:
        """Submits a receipt for processing."""
        receipt_model = ReceiptData(**receipt)
        receipt_id = ReceiptTracker().add_receipt(receipt_model)
        return {"id": receipt_id}
        # 400 error response handled in schema.py by Marshmallow validation check


@receipts_blp.route("/<string:id>/points")
class ReceiptPointsGetResource(MethodView):
    """Defines the points get endpoint."""

    @receipts_blp.doc(
        summary="Returns the points awarded for the receipt.",
        description="Returns the points awarded for the receipt.",
    )
    @receipts_blp.arguments(schema=InputIDSchema, location="path", as_kwargs=True)
    @receipts_blp.response(status_code=HTTPStatus.OK, schema=OutputPointsSchema)
    def get(self: Self, id: str) -> dict:
        """Returns the points awarded for the receipt."""
        try:
            logger.debug(f"Received ID: {id}")
            points = ReceiptTracker().get_points_for_receipt(id)
            logger.debug(f"Calculated points: {points}")
            return {"points": points}
        except NoReceiptFoundException:
            abort(http_status_code=HTTPStatus.NOT_FOUND, message="No receipt found for that ID.")


api.register_blueprint(receipts_blp)
