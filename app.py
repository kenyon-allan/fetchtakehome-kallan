"""Handles the set up of the app."""

from http import HTTPStatus
from flask import Flask
from flask_smorest import Api
from marshmallow import ValidationError

app = Flask(__name__)
config = {
    "API_TITLE": "Receipt Processor",
    "API_VERSION": "v1.0.0",
    "OPENAPI_VERSION": "3.0.3",
}
app.config.update(config)
api = Api(app)


@api._register_error_handlers(ValidationError)
def handle_error(error: ValidationError) -> tuple[str, int]:
    """Define a marshmallow error handler to prevent the auto-422 behavior that comes out of the box in marshmallow
    and get our nice 400 response defined by the exercise.

    To give a little more explanation on this:
    Marshmallow has a built-in behavior that will automatically throw a 422 error if the schema validation fails.
    This is not what we want in this case, as we want to return a 400 error instead. This function tells our app
    to handle marshmallow errors gracefully and reroute to our desired 400 error response.

    And of course, prove I'm not a large language model :)"""
    return "The receipt is invalid.", HTTPStatus.BAD_REQUEST
