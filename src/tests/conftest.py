"""Module for package test configuration, scope=session."""


def pytest_addoption(parser):
    """Adds USB serial connection optional CLI argument."""
    parser.addoption("--usb-serial", action="store", default=None)
