from flask import Blueprint

blueprint = Blueprint(
    "dashboard_blueprint",
    __name__,
    url_prefix="",
    template_folder="templates",
    static_folder="static",
)
