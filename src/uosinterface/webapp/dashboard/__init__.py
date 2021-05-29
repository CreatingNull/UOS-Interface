"""For providing a human-friendly UOS interface."""
from datetime import datetime

from flask import Blueprint
from flask import request
from gevent.event import Event

shutdown_server = Event()

blueprint = Blueprint(
    "dashboard_blueprint",
    __name__,
    url_prefix="",
    template_folder="templates",
    static_folder="static",
)


def get_site_info() -> {}:
    """Function returns useful general data for page rendering."""
    return {"year": datetime.now().year}
