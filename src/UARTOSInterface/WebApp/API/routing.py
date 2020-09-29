from flask import redirect, render_template, request, jsonify
from UARTOSInterface.WebApp.API import blueprint, util
from UARTOSInterface.HardwareCOM import UOSDevice
from logging import getLogger as Log

API_VERSIONS = ["0.0"]


@blueprint.route(f"<string:api_version>/set_gpio_output")
def route_set_gpio_output(api_version: str):
    # todo figure out some general API vetting function
    required_args = {
        "identity": util.APIargument(False, str, None),
        "connection": util.APIargument(False, str, None),
        "pin": util.APIargument(False, int, None),
        "level": util.APIargument(False, int, None),
    }
    response = util.check_required_args(required_args, request.args)
    if response.status:
        device = UOSDevice(
            identity=required_args["identity"].arg_value,
            connection=required_args["connection"].arg_value,
        )
        instr_response = device.set_gpio_output(
            pin=required_args["pin"].arg_value, level=required_args["level"].arg_value,
        )
        response.status = instr_response.status
        response.com_data = instr_response
    return jsonify(response)
