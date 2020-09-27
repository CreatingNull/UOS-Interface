from dataclasses import dataclass, field
from UARTOSInterface.HardwareCOM.util import COMresult


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


def check_required_args(arguments_expected: {}, arguments_found: {}) -> APIresult:
    for argument in arguments_expected:
        if argument not in arguments_found:
            return APIresult(False, f"Expected argument '{argument}' not found in request.")
        try:
            arguments_expected[argument].arg_value = arguments_expected[argument].arg_type(arguments_found[argument])
        except ValueError as e:
            return APIresult(False, f"Expected '{argument}' to have type "
                                    f"{arguments_expected[argument].arg_type} not {type(arguments_found[argument])}.")
    return APIresult(True)



