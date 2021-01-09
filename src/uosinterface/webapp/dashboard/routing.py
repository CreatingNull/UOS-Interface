"""Possible routes for the dashboard functionality of the web-app."""
from collections import defaultdict
from logging import getLogger

from flask import render_template
from flask import request
from flask import session
from uosinterface.hardware import enumerate_devices
from uosinterface.webapp.dashboard import blueprint
from uosinterface.webapp.dashboard import get_site_info
from uosinterface.webapp.dashboard import shutdown_server
from uosinterface.webapp.dashboard.forms import ConnectDeviceForm
from uosinterface.webapp.dashboard.forms import DigitalInstructionForm
from uosinterface.webapp.dashboard.shim import get_system_info


@blueprint.route("/", methods=["GET", "POST"])
@blueprint.route("/device", methods=["GET", "POST"])
def route_device():
    """Index route / device of the dashboard."""
    connect_device_form = ConnectDeviceForm()
    digital_instruction_form = DigitalInstructionForm()
    uos_data = (
        defaultdict(default_factory="")
        if "uos_data" not in session
        else session["uos_data"]
    )
    if connect_device_form.is_submitted():
        getLogger(__name__).debug(
            "route_device %s with %s",
            request.method,
            connect_device_form.device_connection.data,
        )
        uos_data = get_system_info(
            device_identity="Arduino Nano 3",
            device_connection=connect_device_form.device_connection.data,
        )
        session["uos_data"] = uos_data
    return render_template(
        "dashboard/device.html",
        devices=enumerate_devices(),
        uos_data=uos_data,
        connect_device_form=connect_device_form,
        digital_instruction_form=digital_instruction_form,
        site_info=get_site_info(),
    )


@blueprint.route("/settings", methods=["GET"])
def route_settings():
    """Settings control page for the interface."""
    return render_template(
        "dashboard/settings.html",
        devices=enumerate_devices(),
        site_info=get_site_info(),
    )


@blueprint.route("/shutdown", methods=["GET"])
def route_shutdown():
    """Terminates the server execution / interface process."""
    shutdown_server()
    return "UOS Interface server shutting down..."
