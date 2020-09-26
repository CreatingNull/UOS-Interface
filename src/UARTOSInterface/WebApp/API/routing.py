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
    if response["Status"]:
        device = UOSDevice(
            identity=required_args["identity"].arg_value,
            connection=required_args["connection"].arg_value,
        )
        instr_response = device.set_gpio_output(
            pin=int(required_args["pin"].arg_value),
            level=int(required_args["level"].arg_value),
        )
        response["Status"] = instr_response[0]
        response = dict(response, **instr_response[1])
    return jsonify(response)

