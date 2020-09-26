from dataclasses import dataclass


def check_required_args(arguments_expected: {}, arguments_found: {}) -> {}:
    for argument in arguments_expected:
        if argument not in arguments_found:
            return {
                "Status": False,
                "Exception": f"Expected argument '{argument}' not found in request."
            }
        # todo need to implement type vetting on the arguments
        arguments_expected[argument].arg_value = arguments_found[argument]
    return {"Status": True}


@dataclass
class APIargument:
    required: bool
    arg_type: type
    arg_value: None
