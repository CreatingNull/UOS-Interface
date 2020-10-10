"""Web RESTful API layer for automation."""
from flask import request, jsonify
from UARTOSInterface.WebApp.API import blueprint, util
from UARTOSInterface.HardwareCOM import UOSDevice

API_VERSIONS = ["0.0"]


@blueprint.route("<string:api_version>/<string:function>")
def route_io_function(api_version: str, function: str):
    required_args = {
        "pin": util.APIargument(False, int, None),
        "level": util.APIargument(False, int, None),
    }
    response, required_args = util.check_required_args(
        required_args, request.args, add_device=True
    )
    if response.status:
        device = UOSDevice(
            identity=required_args["identity"].arg_value,
            connection=required_args["connection"].arg_value,
        )
        if function in [
            function
            for function in dir(UOSDevice)
            if "get_" in function or "set_" in function
        ]:
            instr_response = getattr(device, function)(
                pin=required_args["pin"].arg_value,
                level=required_args["level"].arg_value,
            )
            response.status = instr_response.status
            response.com_data = instr_response
        else:  # dunno how to handle that function
            response.exception = f"function '{function}' has not been implemented."
            response.status = False
    return jsonify(response)
