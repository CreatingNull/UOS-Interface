"""Possible routes for the dashboard functionality of the web-app."""
from collections import defaultdict
from logging import getLogger

from flask import render_template
from flask import request
from uosinterface.hardware import enumerate_devices
from uosinterface.hardware import UOSDevice
from uosinterface.hardware.config import DEVICES
from uosinterface.webapp.dashboard import blueprint
from uosinterface.webapp.dashboard import shutdown_server
from uosinterface.webapp.dashboard.forms import ConnectDeviceForm


@blueprint.route("/", methods=["GET", "POST"])
@blueprint.route("/device", methods=["GET", "POST"])
def route_device():
    """Index route / device of the dashboard."""
    connect_device_form = ConnectDeviceForm()
    uos_data = defaultdict(default_factory=None)
    if connect_device_form.is_submitted():
        getLogger(__name__).debug(
            "route_device %s with %s",
            request.method,
            connect_device_form.device_connection.data,
        )
        try:
            device = UOSDevice(
                identity="Arduino Nano 3",
                connection=connect_device_form.device_connection.data,
            )
            result = device.get_system_info()
            device.close()
            if result.status:
                uos_data["version"] = (
                    f"V{result.rx_packets[0][4]}.{result.rx_packets[0][5]}."
                    f"{result.rx_packets[0][6]}"
                )
                if f"HWID{result.rx_packets[0][7]}" in DEVICES:
                    uos_data[
                        "type"
                    ] = f"{DEVICES[f'HWID{result.rx_packets[0][7]}'].name}"
        except (AttributeError, ValueError, NotImplementedError) as exception:
            getLogger(__name__).warning(
                "Cannot open connection to '%s', error: %s",
                connect_device_form.device_connection.data,
                exception.__str__(),
            )
    return render_template(
        "dashboard/device.html",
        devices=enumerate_devices(),
        uos_data=uos_data,
        connect_device_form=connect_device_form,
    )


@blueprint.route("/settings", methods=["GET"])
def route_settings():
    """Settings control page for the interface."""
    return render_template("dashboard/settings.html", devices=enumerate_devices())


@blueprint.route("/shutdown", methods=["GET"])
def route_shutdown():
    """Terminates the server execution / interface process."""
    shutdown_server()
    return "UOS Interface server shutting down..."
