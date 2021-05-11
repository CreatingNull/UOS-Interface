"""Package is used to start a simple web-server UOS interface."""
import secrets
from logging import DEBUG
from logging import getLogger as Log
from pathlib import Path

from flask import Flask
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from uosinterface.util import configure_logs
from uosinterface.webapp.api import routing as api_routing
from uosinterface.webapp.dashboard import routing as dashboard_routing
from uosinterface.webapp.database import Base
from uosinterface.webapp.database import engine
from uosinterface.webapp.database import session_maker
from uosinterface.webapp.database import shim

login_manager = LoginManager()
csrf = CSRFProtect()


def register_blueprints(app):
    """Registers the routing for included web-app packages."""
    blueprint_packages = [api_routing, dashboard_routing]
    for blueprint_module in blueprint_packages:
        if hasattr(blueprint_module, "blueprint"):
            app.register_blueprint(blueprint_module.blueprint)


def register_logs(level, base_path: Path):
    """Initialises the logging functionality for the web-app package."""
    configure_logs(__name__, level=level, base_path=base_path)


def register_database(app):
    """Initialise the database functionality for the web-app package."""
    app.config["DATABASE"] = {"ENGINE": engine, "SESSION_MAKER": session_maker}

    @login_manager.user_loader
    def load_user(user_id):
        return shim.get_user(name_id=user_id, session_maker=app.config)

    @login_manager.request_loader
    def request_loader(request):
        username = request.form.get("username")
        user = load_user(username)
        return user if user else None

    @app.before_first_request
    def initialise_database(exception=None):
        Base.metadata.create_all(app.config["DATABASE"]["ENGINE"])

    @app.teardown_appcontext
    def shutdown_database(exception=None):
        app.config["DATABASE"]["ENGINE"].dispose()


def create_app(testing: bool, base_path: Path, static_path: Path):
    """Creates the flask app and registers all addons."""
    app = Flask(
        __name__,
        static_folder=static_path.__str__(),
        template_folder=static_path.joinpath(Path("templates/")).__str__(),
    )
    csrf.init_app(app)
    app.config["TESTING"] = testing
    app.config["SECRET_KEY"] = secrets.token_urlsafe(32)
    register_database(app)
    register_blueprints(app)
    register_logs(DEBUG, base_path=base_path)
    Log(__name__).debug("Static resolved to %s", static_path.__str__())
    return app
