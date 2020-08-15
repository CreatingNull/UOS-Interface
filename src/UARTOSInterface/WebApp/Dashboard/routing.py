from flask import url_for, redirect, render_template
from UARTOSInterface.WebApp.Dashboard import blueprint
from UARTOSInterface.HardwareCOM import UOSDevice
from logging import getLogger as Log


@blueprint.route('/')
def route_default():
    device = UOSDevice('Arduino Nano 3', connection='/dev/ttyUSB0')
    Log(__name__).debug(f"{device} created")
    device.close()
    return render_template("site_template/base_site.html")
