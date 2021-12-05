# ![NullTek Documentation](resources/UOSLogoSmall.png) UOS Interface

[![License](https://img.shields.io/:license-mit-blue.svg?style=flat-square)](LICENSE.md)
[![Codacy Inspection](https://app.codacy.com/project/badge/Grade/8a24020489ee4638aa10449e3f1cc0cd)](https://www.codacy.com/gh/CreatingNull/UOS-Interface/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=CreatingNull/UOS-Interface&amp;utm_campaign=Badge_Grade)
[![Codacy Converge](https://app.codacy.com/project/badge/Coverage/8a24020489ee4638aa10449e3f1cc0cd)](https://www.codacy.com/gh/CreatingNull/UOS-Interface/dashboard?utm_source=github.com&utm_medium=referral&utm_content=CreatingNull/UOS-Interface&utm_campaign=Badge_Coverage)
[![Documentation Status](https://readthedocs.org/projects/uos-interface/badge/?version=latest)](https://uos-interface.nulltek.xyz/en/latest/?badge=latest)
[![Tests Badge](https://github.com/CreatingNull/UOS-Interface/actions/workflows/run-tests.yml/badge.svg)](https://github.com/CreatingNull/UOS-Interface/actions/workflows/run-tests.yml)

Python Interface for remote communication and control of a UOS Compliant Microcontroller.

Status: Still under development, not ready for a release yet.

---

## Dependencies

The project backend is written using Python Flask.
Backend requirements can be found in [requirements.txt](resources/requirements.txt).

```pip install -r resources/requirements.txt```

The project front end is vanilla javascript, html and css.
Frontend requirements:
*   FontAwesome 5.15.1 Web - for development this should be nested in `src/uosinterface/webapp/static/lib/FontAwesome`

## Contributing

For code formatting project uses [pre-commit](https://github.com/CreatingNull/UOS-Interface/actions/workflows/run-pre-commit.yml), see repo [hooks](pre-commit-config.yaml).
This code also uses a pytest [test suite](https://github.com/CreatingNull/UOS-Interface/actions/workflows/run-tests.yml).

Both these actions are currently automated by GitHub actions CI, and run on pushes and pull-requests.

## Donations

I just do this stuff for fun in my spare time, but feel free to:

[![Support via buymeacoffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/nulltek)

---

## License

The source of this repo uses the MIT open-source license, for details on the current licensing see LICENSE.md or click the badge above.
*   Copyright 2021 © <a href="https://nulltek.xyz" target="_blank">NullTek</a>.
