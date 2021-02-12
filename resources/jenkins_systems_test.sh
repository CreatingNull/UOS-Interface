#!/bin/sh

# Shell script for configuring the UOS-Jenkins system's test rack.
# This is for testing coverage of hardware layers and interfaces.

/opt/python/bin/python3.9 -m venv venv/
ci_python=venv/bin/python
$ci_python -m pip install --upgrade pip
$ci_python -m pip install --upgrade setuptools
$ci_python -m pip install -r resources/requirements.txt
$ci_python -m pip install wheel
$ci_python -m pip install pytest
$ci_python -m pip install coverage
$ci_python -m coverage run --rc-file=coveragerc.ini -m pytest src/tests/ --usb-serial=/dev/ttyUSB0
$ci_python -m coverage xml --rc-file=coveragerc.ini
