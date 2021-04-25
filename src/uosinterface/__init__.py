"""Package for UOS Interface, module contains exception classes."""


class UOSError(Exception):
    """Base class exception for all UOS Interface Errors."""


class UOSUnsupportedError(UOSError):
    """Exception for attempting an unknown / unsupported action."""


class UOSCommunicationError(UOSError):
    """Exception while communicating with a UOS Device."""


class UOSConfigurationError(UOSError):
    """Exception caused by the setup / config of the UOS Device."""
