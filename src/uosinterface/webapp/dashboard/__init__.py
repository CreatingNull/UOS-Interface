"""For providing a human-friendly UOS interface."""
from datetime import datetime

from flask import Blueprint
from flask import request

blueprint = Blueprint(
    "dashboard_blueprint",
    __name__,
    url_prefix="",
    template_folder="templates",
    static_folder="static",
)


def shutdown_server():
    """Function stops the server execution."""
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


def get_site_info() -> {}:
    """Function returns useful general data for page rendering."""
    return {"year": datetime.now().year}
