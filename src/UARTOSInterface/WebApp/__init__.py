import configparser
from pathlib import Path
from flask import Flask
from importlib import import_module
from logging import getLogger as Log, DEBUG
from UARTOSInterface.util import configure_logs


def register_blueprints(app):
    project_modules = ["Dashboard"]
    for module_name in project_modules:
        module = import_module(f"UARTOSInterface.WebApp.{module_name}.routing")
        if hasattr(module, "blueprint"):
            app.register_blueprint(module.blueprint)


def load_config(path: Path):
    Log(__name__).debug(f"Loading config from {path}")
    parser = configparser.ConfigParser()
    parser.read(str(path.resolve()))
    if len(parser.sections()) > 0:  # config was located
        return parser
    return None


def register_logs(level, base_path: Path):
    configure_logs(__name__, level=level, base_path=base_path)


def create_app(conf: configparser.ConfigParser, base_path: Path):
    app = Flask(__name__, static_folder="static", template_folder="static/templates")
    app.config["TESTING"] = conf.getboolean("Flask Config", "TESTING"),
    app.config["SECRET_KEY"] = conf["Flask Config"]["SECRET_KEY"]
    register_blueprints(app)
    register_logs(DEBUG, base_path=base_path)
    return app
