import configparser
from pathlib import Path
from flask import Flask
from importlib import import_module
from util import configure_logs, configure_root_stream, DEBUG, INFO
from HardwareCOM import init_logs as init_hardware_logs


def init_interface_logs(level: int):
    configure_logs(__name__, level)


def register_blueprints(app):
    project_modules = ['Dashboard']
    for module_name in project_modules:
        module = import_module('UARTOSInterface.{}.routing'.format(module_name))
        app.register_blueprint(module.blueprint)


def load_config(path: Path):
    parser = configparser.ConfigParser()
    parser.read(str(path.resolve()))
    if len(parser.sections()) > 0:  # config was located
        return parser
    return None


def create_app(conf: configparser.ConfigParser, base_dir: Path):
    configure_root_stream(INFO)  # stderr streamed on base logger
    init_interface_logs(DEBUG)  # per module custom log files
    init_hardware_logs(DEBUG)
    app = Flask(__name__, static_folder="static", template_folder="static/templates")
    app.config["TESTING"] = conf.getboolean("Flask Config", "TESTING"),
    app.config["SECRET_KEY"] = conf["Flask Config"]["SECRET_KEY"]
    register_blueprints(app)
    return app
