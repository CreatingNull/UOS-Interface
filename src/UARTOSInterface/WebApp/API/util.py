from dataclasses import dataclass
from UARTOSInterface.HardwareCOM.UOSInterface import COMresult
from logging import getLogger as Log


@dataclass
class APIargument:
    required: bool
    arg_type: type
    arg_value: None


@dataclass
class APIresult:
    status: bool
    exception: str = ""
    com_data: COMresult = None


def check_required_args(
    required_arguments: {}, arguments_found: {}, add_device: bool = False
) -> (APIresult, {}):
    if add_device:
        required_arguments = dict(
            required_arguments,
            **{
                "identity": APIargument(False, str, None),
                "connection": APIargument(False, str, None),
            },
        )
    Log(__name__).debug(f"Required arguments {required_arguments.__str__()}")
    for argument in required_arguments:
        if argument not in arguments_found:
            return APIresult(
                False, f"Expected argument '{argument}' not found in request."
            )
        try:
            required_arguments[argument].arg_value = required_arguments[
                argument
            ].arg_type(arguments_found[argument])
        except ValueError:
            return APIresult(
                False,
                f"Expected '{argument}' to have type "
                f"{required_arguments[argument].arg_type} not {type(arguments_found[argument])}.",
            )
    return APIresult(True), required_arguments
