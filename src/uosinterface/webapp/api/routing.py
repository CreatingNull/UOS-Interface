"""Web RESTful API layer for automation."""
import inspect

from flask import jsonify
from flask import request
from uosinterface.hardware import COMresult
from uosinterface.hardware import UOSDevice
from uosinterface.webapp.api import API_VERSIONS
from uosinterface.webapp.api import blueprint
from uosinterface.webapp.api import util


@blueprint.route("<string:api_version>/<string:function>")
def route_hardware_function(api_version: str, function: str):
    """Can be used to execute standard UOS IO functions."""
    if api_version not in API_VERSIONS:
        return jsonify(
            COMresult(
                False,
                exception=f"'{function}' not supported in api version {api_version}.",
            )
        )
    try:
        arguments = inspect.signature(getattr(UOSDevice, function))
    except AttributeError as e:
        return jsonify(
            COMresult(
                False, exception=f"API call on '{function}' threw error {e.__str__()}."
            )
        )
    possible_args = {
        argument.name: util.APIargument(
            argument.default == inspect.Parameter.empty, argument.annotation, None
        )
        for argument in arguments.parameters.values()
        if argument.name != "self" and argument.name != "kwargs"
    }
    response, required_args = util.check_required_args(
        possible_args, request.args, add_device=True
    )
    if response.status:
        device = UOSDevice(
            identity=required_args["identity"].arg_value,
            connection=required_args["connection"].arg_value,
        )
        if function in dir(UOSDevice):
            instr_response = getattr(device, function)(
                *[
                    required_args[parameter.name].arg_value
                    for parameter in inspect.signature(
                        getattr(device, function)
                    ).parameters.values()
                    if parameter.name in required_args
                    and required_args[parameter.name].arg_value is not None
                ]
            )
            response.status = instr_response.status
            response.com_data = instr_response
        else:  # dunno how to handle that function
            response.exception = f"function '{function}' has not been implemented."
            response.status = False
    return jsonify(response)
