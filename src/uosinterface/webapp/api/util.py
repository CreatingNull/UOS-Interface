"""General utility functions for the API layer of the web-server."""
from dataclasses import dataclass
from logging import getLogger as Log

from uosinterface.hardware.uosabstractions import COMresult


@dataclass
class APIargument:
    """API request argument datatype."""

    required: bool
    arg_type: type
    arg_value: None


@dataclass
class APIresult:
    """The response from an API request to be returned as JSON."""

    status: bool
    exception: str = ""
    com_data: COMresult = None


def check_required_args(
    required_arguments: {}, arguments_found: {}, add_device: bool = False
) -> (APIresult, {}):
    """Adds common arguments and vets user request against parameters."""
    if add_device:
        required_arguments = dict(
            required_arguments,
            **{
                "identity": APIargument(False, str, None),
                "connection": APIargument(False, str, None),
            },
        )
    Log(__name__).debug("Required arguments %s", required_arguments.__str__())
    for argument in required_arguments:
        if argument not in arguments_found:
            return (
                APIresult(
                    False, f"Expected argument '{argument}' not found in request."
                ),
                required_arguments,
            )
        try:
            required_arguments[argument].arg_value = required_arguments[
                argument
            ].arg_type(arguments_found[argument])
        except ValueError:
            return (
                APIresult(
                    False,
                    f"Expected '{argument}' to have type {required_arguments[argument].arg_type} "
                    f"not {type(arguments_found[argument])}.",
                ),
                required_arguments,
            )
    return APIresult(True), required_arguments
