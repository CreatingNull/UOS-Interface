"""Package is used to start a simple web-server UOS interface."""
import configparser
from importlib import import_module
from logging import DEBUG
from pathlib import Path

from flask import Flask
from UARTOSInterface.util import configure_logs


def register_blueprints(app):
    """Registers the routing for included web-app packages."""
    blueprint_packages = ["API", "Dashboard"]
    for module_name in blueprint_packages:
        module = import_module(f"UARTOSInterface.WebApp.{module_name}.routing")
        if hasattr(module, "blueprint"):
            app.register_blueprint(module.blueprint)


def register_logs(level, base_path: Path):
    """Initialises the logging functionality for the Webapp package."""
    configure_logs(__name__, level=level, base_path=base_path)


def create_app(conf: configparser.ConfigParser, base_path: Path):
    """Creates the flask app and registers all addons."""
    app = Flask(__name__, static_folder="static", template_folder="static/templates")
    app.config["TESTING"] = (conf.getboolean("Flask Config", "TESTING"),)
    app.config["SECRET_KEY"] = conf["Flask Config"]["SECRET_KEY"]
    register_blueprints(app)
    register_logs(DEBUG, base_path=base_path)
    return app
