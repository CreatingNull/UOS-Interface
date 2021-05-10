"""Package for UOS Interface, module contains exception classes."""
import sys
from pathlib import Path

# path used to refer to the root directory of the app.
if getattr(sys, "frozen", False):  # in deployment
    base_dir = Path(sys.executable).parent
    static_dir = base_dir.joinpath("static/")
else:  # development
    base_dir = Path(__file__).parents[2]
    static_dir = base_dir.joinpath("src/uosinterface/webapp/static/")
# path used to refer to resources folder of the app.
resources_path = base_dir.joinpath(Path("resources"))


class UOSError(Exception):
    """Base class exception for all UOS Interface Errors."""


class UOSUnsupportedError(UOSError):
    """Exception for attempting an unknown / unsupported action."""


class UOSCommunicationError(UOSError):
    """Exception while communicating with a UOS Device."""


class UOSConfigurationError(UOSError):
    """Exception caused by the setup / config of the UOS Device."""
