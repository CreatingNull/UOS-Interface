#!/bin/sh

# Shell script for configuring the UOS-Jenkins system's test rack.
# This is for testing coverage of hardware layers and interfaces.

/opt/python/bin/python3.9 -m venv venv/
ci_python=venv/bin/python
$ci_python -m pip install --upgrade pip
$ci_python -m pip install --upgrade setuptools
$ci_python -m pip install -r resources/requirements.txt
$ci_python -m pip install pytest
$ci_python -m pip install coverage
$ci_python -m pytest src/tests/
