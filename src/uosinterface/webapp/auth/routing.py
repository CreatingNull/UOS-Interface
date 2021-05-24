"""Flask webapp routing module for authentication functionality."""
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from uosinterface.webapp.auth import blueprint
from uosinterface.webapp.dashboard import get_site_info  # todo rethink this
from uosinterface.webapp.database import interface as db_interface
from uosinterface.webapp.database import verify_pass
from uosinterface.webapp.database.models import User
from uosinterface.webapp.forms import AuthForm


@blueprint.route("/", methods=["GET", "POST"])
@blueprint.route("/login", methods=["GET", "POST"])
def route_login():
    """Handles index routing and user session based authentication."""
    login_form = AuthForm()
    if request.method == "POST":
        if login_form.validate():
            with current_app.config["DATABASE"]["SESSION"]() as session:
                user = db_interface.get_user(
                    session=session,
                    user_value=login_form.name.data,
                    user_field=User.name,
                )
            if user and verify_pass(login_form.passwd.data, user.pass_hash):
                flash(f"Welcome {user.name}.")
                login_user(user)
            else:
                flash("Invalid username or password!", category="warning")
        else:
            flash("Invalid data entered", category="error")
    if current_user.is_authenticated:
        return redirect(url_for("dashboard_blueprint.route_device"))
    return render_template(
        "auth/form.html",
        auth_action="Log In",
        auth_form=login_form,
        site_info=get_site_info(),
    )


@blueprint.route("/logout")
def route_logout():
    """Route to terminate user session."""
    logout_user()
    return redirect(url_for("auth_blueprint.route_login"))


@blueprint.route("/error")
@blueprint.errorhandler(404)
def route_error(error):
    """Route for managing templated http error responses."""
    return f"error {error}"
