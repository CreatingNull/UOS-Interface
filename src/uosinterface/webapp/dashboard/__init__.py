"""For providing a human-friendly UOS interface."""
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
