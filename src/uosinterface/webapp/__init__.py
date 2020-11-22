"""Package is used to start a simple web-server UOS interface."""
import secrets
from importlib import import_module
from logging import DEBUG
from pathlib import Path

import uosinterface.webapp.api.routing as api_routing
import uosinterface.webapp.dashboard.routing as dashboard_routing
from flask import Flask
from uosinterface.util import configure_logs


def register_blueprints(app):
    """Registers the routing for included web-app packages."""
    blueprint_packages = [api_routing, dashboard_routing]
    for blueprint_module in blueprint_packages:
        if hasattr(blueprint_module, "blueprint"):
            app.register_blueprint(blueprint_module.blueprint)


def register_logs(level, base_path: Path):
    """Initialises the logging functionality for the Webapp package."""
    configure_logs(__name__, level=level, base_path=base_path)


def create_app(testing: bool, base_path: Path):
    """Creates the flask app and registers all addons."""
    app = Flask(__name__, static_folder="static", template_folder="static/templates")
    app.config["TESTING"] = testing
    app.config["SECRET_KEY"] = secrets.token_urlsafe(32)
    register_blueprints(app)
    register_logs(DEBUG, base_path=base_path)
    return app
