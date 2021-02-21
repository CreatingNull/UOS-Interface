#!/bin/bash

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
$ci_python -m coverage run --rcfile=.coveragerc.ini -m pytest src/tests/ --usb-serial=/dev/ttyUSB0
$ci_python -m coverage xml --rcfile=.coveragerc.ini

# After this coverage report is uploaded to codacy project against the commit hash
# API Token must already be injected as protected environment variable.
# shellcheck disable=SC1019
if [[ -n "${CODACY_PROJECT_TOKEN}" ]]; then
  curl -LS -o codacy-coverage-reporter-assembly.jar "$(curl -LSs https://api.github.com/repos/codacy/codacy-coverage-reporter/releases/latest | jq -r '.assets | map({name, browser_download_url} | select(.name | endswith(".jar"))) | .[0].browser_download_url')"
  java -jar codacy-coverage-reporter-assembly.jar report --commit-uuid "$COMMIT_ID" -r ../logs/coverage/coverage.xml.
fi
