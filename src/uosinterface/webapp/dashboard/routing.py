"""Possible routes for the dashboard functionality of the web-app."""
import json
from collections import defaultdict
from logging import getLogger

from flask import make_response
from flask import render_template
from flask import request
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
        json.loads(request.cookies.get("uos_data"))
        if "uos_data" in request.cookies
        else {}
    )
    if connect_device_form.is_submitted():  # connect and query device info
        getLogger(__name__).debug(
            "route_device %s with %s",
            request.method,
            connect_device_form.__repr__(),
        )
        uos_data.update(
            get_system_info(  # get the system type and version info
                device_identity="Arduino Nano 3",
                device_connection=connect_device_form.device_connection.data,
            )
        )
    elif digital_instruction_form.is_submitted():  # execute a digital_instruction]
        getLogger(__name__).debug(
            "route_device digital command %s with %s",
            request.method,
            digital_instruction_form.__repr__(),
        )
    resp = make_response(
        render_template(
            "dashboard/device.html",
            devices=enumerate_devices(),
            uos_data=uos_data,
            connect_device_form=connect_device_form,
            digital_instruction_form=digital_instruction_form,
            site_info=get_site_info(),
        )
    )
    resp.set_cookie("uos_data", json.dumps(uos_data), samesite="Strict")
    return resp


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
