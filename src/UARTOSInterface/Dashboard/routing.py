from flask import url_for, redirect, render_template
from UARTOSInterface.Dashboard import blueprint
from HardwareCOM import UOSDevice
from util import log, DEBUG, INFO, WARNING, ERROR

@blueprint.route('/')
def route_default():
    device = UOSDevice('Arduino Nano 3', connection='/dev/ttyUSB0')
    log(f"{device} created", level=DEBUG, name=__name__)
    device.close()
    return render_template("site_template/base_site.html")
