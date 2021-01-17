"""API Package blueprint initialisations."""
from flask import Blueprint

API_VERSIONS = ["0.0"]

blueprint = Blueprint(
    "api_blueprint",
    __name__,
    url_prefix="/api",
    template_folder="api",
    static_folder="static",
)
