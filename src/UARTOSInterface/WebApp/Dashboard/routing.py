"""Possible routes for the dashboard functionality of the web-app."""
from flask import render_template
from UARTOSInterface.HardwareCOM import enumerate_devices
from UARTOSInterface.WebApp.Dashboard import blueprint
from UARTOSInterface.WebApp.Dashboard import shutdown_server


@blueprint.route("/")
def route_default():
    """Index route / home page of the dashboard."""
    return render_template("site_template/base_site.html", devices=enumerate_devices())


@blueprint.route("/shutdown", methods=["GET"])
def route_shutdown():
    """Terminates the server execution / interface process."""
    shutdown_server()
    return "UOS Interface server shutting down..."
