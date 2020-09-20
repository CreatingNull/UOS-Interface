from flask import redirect, render_template
from UARTOSInterface.WebApp.Dashboard import blueprint
from UARTOSInterface.HardwareCOM import UOSDevice
from logging import getLogger as Log


@blueprint.route('/')
def route_default():
    device = UOSDevice('Arduino Nano 3', connection='USB|/dev/ttyUSB0')
    device.set_gpio_output(13, 1)
    Log(__name__).debug(f"{device} created")
    return render_template("site_template/base_site.html")


@blueprint.route("/on")
def route_on():
    device = UOSDevice('Arduino Nano 3', connection='USB|/dev/ttyUSB0')
    response = device.set_gpio_output(13, 1)
    return {"Status": response[0], **response[1]}


@blueprint.route("/off")
def route_off():
    device = UOSDevice('Arduino Nano 3', connection='USB|/dev/ttyUSB0')
    response = device.set_gpio_output(13, 0)
    return {"Status": response[0], **response[1]}


@blueprint.route("/reset")
def route_reset():
    device = UOSDevice('Arduino Nano 3', connection='USB|/dev/ttyUSB0')
    device.hard_reset()
    return "reset"


@blueprint.route("/read")
def route_read():
    device = UOSDevice('Arduino Nano 3', connection='USB|/dev/ttyUSB0')
    response = device.get_gpio_input(10, 0)
    return {"Status": response[0], **response[1]}
