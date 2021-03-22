"""Package for UOS Interface, module contains exception classes."""


class UOSError(Exception):
    """Base class exception for all UOS Interface Errors."""

    pass


class UOSUnsupportedError(UOSError):
    """Exception for attempting an unknown / unsupported action."""

    pass


class UOSCommunicationError(UOSError):
    """Exception while communicating with a UOS Device."""

    pass


class UOSConfigurationError(UOSError):
    """Exception caused by the setup / config of the UOS Device."""

    pass
