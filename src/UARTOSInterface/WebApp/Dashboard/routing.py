from flask import redirect, render_template
from UARTOSInterface.WebApp.Dashboard import blueprint
from UARTOSInterface.HardwareCOM import UOSDevice
from logging import getLogger as Log


@blueprint.route("/")
def route_default():
    device = UOSDevice("Arduino Nano 3", connection="USB|/dev/ttyUSB0")
    device.set_gpio_output(13, 1)
    Log(__name__).debug(f"{device} created")
    return render_template("site_template/base_site.html")
