"""Possible routes for the dashboard functionality of the web-app."""
from logging import getLogger as Log

from flask import render_template
from UARTOSInterface.HardwareCOM import UOSDevice
from UARTOSInterface.WebApp.Dashboard import blueprint
from UARTOSInterface.WebApp.Dashboard import shutdown_server


@blueprint.route("/")
def route_default():
    """Index route / home page of the dashboard."""
    device = UOSDevice("Arduino Nano 3", connection="USB|/dev/ttyUSB0")
    device.set_gpio_output(13, 1)
    Log(__name__).debug("%s created", device)
    return render_template("site_template/base_site.html")


@blueprint.route("/shutdown", methods=["GET"])
def route_shutdown():
    """Terminates the server execution / interface process."""
    shutdown_server()
    return "UOS Interface server shutting down..."
