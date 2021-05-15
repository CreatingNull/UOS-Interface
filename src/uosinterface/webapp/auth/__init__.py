"""Authentication Package blueprint initialisations."""
from functools import wraps
from logging import getLogger as Log

from flask import Blueprint
from flask import url_for


def privileged_route(current_user, privilege_names: [] = ()):
    """
    Route decorator to check user / API access.

    :param current_user: The current user object for the session.
    :param privilege_names: List of names of privileges with access, empty means logged in.
    :return: Wrapped function with authentication behaviour applied.

    """

    def decorator(func):
        @wraps(func)
        def check_privileges(*args, **kwargs):
            """
            Function for checking a user's privileges match requirements.

            :param args: Wrapped function's positional arguments.
            :param kwargs: Wrapped function's keyword arguments.
            :return: Function if authorised, otherwise redirects to an error.

            """
            if not current_user.is_authenticated:
                Log(__name__).info(
                    f"Attempt to access {func.__name__} protected route while not logged in."
                )
                return url_for("auth_blueprint.route_error", error=401)
            Log(__name__).debug(f"Checking user privileges for {current_user.name}")
            if len(privilege_names) == 0:  # essentially just login_required
                return func(*args, **kwargs)
            return url_for("auth_blueprint.route_error", error=401)

        return check_privileges

    return decorator


blueprint = Blueprint(
    "auth_blueprint",
    __name__,
    url_prefix="",
    template_folder="templates",
    static_folder="static",
)
