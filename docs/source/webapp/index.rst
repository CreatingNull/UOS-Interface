.. Documenting the use of the web app package

======
Webapp
======

The webapp package simultaneously serves a dashboard and an API for control of UOS hardware.

Dashboard
---------

The UOS Interface can be configured and used entirely a graphical web-dashboard interface.

API Automation Layer
--------------------

The UOS Interface supports automated control of UOS devices through a RESTful web API.
This API interface exists on the url :code:`http://served-address/api`.

The interface is designed to be replicate the functionality of the :doc:`../hardware/index`.
To achieve stateless operation all API operations are self-contained and stand-alone.

Example Usage:

The standard format is :code:`http://served-address/api/version/instruction?device_arguments&instruction_arguments`

*	`version` - Define the API version to use, certain UOS versions and API levels may not be compatible.
*	`instruction` - Provides the name of the instruction being used from the hardware abstraction layer.
*	`device_arguments` - Must provide address and identity at minimum.
*	`instruction_arguments` - Must provide all non-optional arguments for the HAL instruction being used.

Note: Arguments can be provided in any order but must all be seperated using the URL :code:`&` delimiter.

Example Usage:

This is the `hello world` usage for turning on the arduino on-board pin 13 LED.

:code:`http://served-address/api/1.0/set_gpio_output?address=/dev/ttyUSB0&identity=arduino_nano&pin=13&level=1`

