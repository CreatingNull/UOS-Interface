from flask import Blueprint

blueprint = Blueprint(
    'api_blueprint',
    __name__,
    url_prefix="/api",
    template_folder="api",
    static_folder="static",
)
