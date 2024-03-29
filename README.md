# ![NullTek Documentation](resources/UOSLogoSmall.png) UOS Interface

[![License](https://img.shields.io/:license-mit-blue.svg?style=flat-square)](LICENSE.md)

This project is no longer maintained and superseded by:

* [uos-hardware](https://github.com/CreatingNull/UOS-Hardware) - Hardware abstraction layer for handling low-level devices and interfaces.

---

Python Interface for remote communication and control of a UOS Compliant Microcontroller.

---

## Dependencies

The project backend is written using Python Flask.
Backend requirements can be found in [requirements.txt](resources/requirements.txt).

```pip install -r resources/requirements.txt```

The project front end is vanilla javascript, html and css.
Frontend requirements:
*   FontAwesome 5.15.1 Web - for development this should be nested in `src/uosinterface/webapp/static/lib/FontAwesome`

## Contributing

For code formatting this project uses [pre-commit](https://github.com/CreatingNull/UOS-Interface/actions/workflows/run-pre-commit.yml), see repo [hooks](.pre-commit-config.yaml).
This code also uses a pytest [test suite](https://github.com/CreatingNull/UOS-Interface/actions/workflows/run-tests.yml).

Both these actions are currently automated by GitHub actions CI, and run on pushes and pull-requests.

## Donations

I just do this stuff for fun in my spare time, but feel free to:

[![Support via buymeacoffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/nulltek)

---

## License

The source of this repo uses the MIT open-source license, for details on the current licensing see [LICENSE](LICENSE.md) or click the badge above.
