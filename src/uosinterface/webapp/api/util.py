"""General utility functions for the API layer of the web-server."""
from dataclasses import dataclass
from logging import getLogger as Log

from uosinterface.hardware.uosabstractions import ComResult


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
    com_data: ComResult = None


def check_required_args(
    possible_arguments: dict[APIargument],
    arguments_found: dict,
    add_device: bool = False,
) -> (APIresult, dict):
    """Adds common arguments and vets user request against parameters."""
    if add_device:
        possible_arguments = dict(
            possible_arguments,
            **{
                "identity": APIargument(True, str, None),
                "connection": APIargument(True, str, None),
            },
        )
    for argument in possible_arguments:
        if argument not in arguments_found and possible_arguments[argument].required:
            return (
                APIresult(
                    False, f"Required argument '{argument}' not found in request."
                ),
                possible_arguments,
            )
        try:
            if argument in arguments_found:
                possible_arguments[argument].arg_value = possible_arguments[
                    argument
                ].arg_type(arguments_found[argument])
        except ValueError:
            return (
                APIresult(
                    False,
                    f"Expected '{argument}' to have type {possible_arguments[argument].arg_type} "
                    f"not {type(arguments_found[argument])}.",
                ),
                possible_arguments,
            )
    Log(__name__).debug("API arguments %s", possible_arguments.__str__())
    return APIresult(True), possible_arguments
