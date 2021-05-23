"""Authentication Package blueprint initialisations."""
from enum import Enum
from functools import wraps
from logging import getLogger as Log

from flask import Blueprint
from flask import current_app
from flask import url_for
from flask_login import current_user
from uosinterface.webapp.database.interface import get_user_privileges


blueprint = Blueprint(
    "auth_blueprint",
    __name__,
    url_prefix="",
    template_folder="templates",
    static_folder="static",
)


class PrivilegeNames(Enum):

    ADMIN = 1  # Full System Privileges
    VIEW = 2  # Can navigate and view but not adjust settings.


def privileged_route(privilege_names: [PrivilegeNames] = ()):
    """
    Flask route decorator to check user / API access.

    :param privilege_names: List of names of privileges with access, empty means logged in.
    :return: Wrapped function with authentication behaviour applied.

    """

    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            """
            Handling web-app route selection for the wrapped route.

            :param args: Wrapped function's positional arguments.
            :param kwargs: Wrapped function's keyword arguments.
            :return: Wrapped route if authorised, otherwise redirect to error.

            """
            with current_app.config["DATABASE"]["SESSION"]() as session:
                if check_privileges(privilege_names, session, current_user):
                    Log(__name__).debug(f"Authenticated {current_user.name}")
                    return func(*args, **kwargs)
            Log(__name__).info(
                f"Attempt to access {func.__name__} protected route while not logged in."
            )
            return url_for("auth_blueprint.route_error", error=401)

        return wrapped_function

    return decorator


def check_privileges(privilege_names: [], session, user) -> bool:
    """
    Function for checking a user's privileges match requirements. Authorised if
    no privilege names in argument and user is logged in. Authorised if user
    has listed privilege or admin.

    :param: List of names of privileges with access, empty means logged in.
    :param: SQLAlchemy session instance to lookup user privileges.
    :param: User to check against privilege list.
    :return: True if authorised, False otherwise.

    """
    if not user.is_authenticated:
        return False
    Log(__name__).debug(f"Checking user privileges for {user.name}")
    if len(privilege_names) == 0:  # essentially just login_required
        return True
    # iterate through privileges of user and check for a match
    user_privileges = get_user_privileges(session, user.id)
    Log(__name__).debug(
        f"Has privileges {[user_privilege.name for user_privilege in user_privileges]}"
    )
    for user_privilege in user_privileges:
        if (
            user_privilege.name
            in [privilege_name for privilege_name in privilege_names]
            or user_privilege.name == PrivilegeNames.ADMIN.name
        ):
            return True
    return False
