"""Possible routes for the dashboard functionality of the web-app."""
from flask import render_template
from uosinterface.hardware import enumerate_devices
from uosinterface.webapp.dashboard import blueprint
from uosinterface.webapp.dashboard import shutdown_server


@blueprint.route("/")
@blueprint.route("/device")
def route_device():
    """Index route / device of the dashboard."""
    return render_template("dashboard/device.html", devices=enumerate_devices())


@blueprint.route("/settings")
def route_settings():
    """Settings control page for the interface."""
    return render_template("dashboard/settings.html", devices=enumerate_devices())


@blueprint.route("/shutdown", methods=["GET"])
def route_shutdown():
    """Terminates the server execution / interface process."""
    shutdown_server()
    return "UOS Interface server shutting down..."
