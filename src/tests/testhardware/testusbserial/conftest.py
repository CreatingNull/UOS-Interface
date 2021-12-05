"""Module used for argument / test initialisation of low level serial
driver."""
import pytest


@pytest.fixture(scope="package")
def usb_serial_argument(request):
    """Create a serial fixture if --usb-serial argument provided to CLI."""
    usb_serial_connection = request.config.option.usb_serial
    if usb_serial_connection is None:
        pytest.skip("Low level hardware only tested if connection is provided to test.")
    return usb_serial_connection
