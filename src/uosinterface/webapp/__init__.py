"""Package is used to start a simple web-server UOS interface."""
import secrets
from functools import wraps
from logging import DEBUG
from logging import getLogger as Log
from pathlib import Path

from flask import _app_ctx_stack
from flask import Flask
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from sqlalchemy.orm import scoped_session
from uosinterface.util import configure_logs
from uosinterface.webapp.api import routing as api_routing
from uosinterface.webapp.dashboard import routing as dashboard_routing
from uosinterface.webapp.database import Base
from uosinterface.webapp.database import engine
from uosinterface.webapp.database import session_maker
from uosinterface.webapp.database import shim
from uosinterface.webapp.database.models import User
from uosinterface.webapp.database.models import UserKeys

login_manager = LoginManager()
csrf = CSRFProtect()


def privileged_route(func, privilege_names: []):
    """
    Route decorator to check user / API access.

    :param func: Implicit function being wrapped.
    :param privilege_names: List of names of privileges with access, empty means logged in.
    :return: Wrapped function with authentication behaviour applied.

    """

    @wraps(func)
    def check_privileges(*args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """

    return check_privileges


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
    app.config["DATABASE"] = {
        "ENGINE": engine,
        # Unique requests should get unique sessions.
        # The same request should get the same session.
        "SESSION": scoped_session(
            session_maker, scopefunc=_app_ctx_stack.__ident_func__
        ),
    }

    @login_manager.user_loader
    def load_user(user_id):
        return shim.get_user(
            session_maker=app.config["DATABASE"]["SESSION"], identifier=user_id
        )

    @login_manager.request_loader
    def request_loader(request):
        """Auth handling using the request header."""
        api_key = request.args.get("api_key")
        if api_key:
            user = shim.get_user(
                app.config["DATABASE"]["SESSION"],
                identifier=api_key,
                user_field=UserKeys.key,
            )
            if user:
                return user
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
