Hardware Abstraction
====================

The UOS interface hardware abstraction layer provides a common interface for control of UOS devices.

Supported Hardware
------------------

Supported devices are enumerated and defined in `uosinterface.hardware.devices.py`.

All devices are defined using the `Devices` abstraction class.

.. autoclass:: uosinterface.hardware.uosabstractions.Device
	:members:

Abstraction Layer
-----------------

Devices can be accessed through the hardware layer by instantiating a `UOSDevice`.
By default the device is used in a lazy manner, where references to the interface opened and closed automatically as required for functions.

Example usage:

.. code-block:: python

	from uosinterface.hardware import UOSDevice
	from uosinterface.hardware.devices import ARDUINO_NANO_3
	from uosinterface.hardware.devices import Interface

	device = UOSDevice(
		identity = ARDUINO_NANO_3,
		address = "/dev/ttyUSB0",
		interface = Interface.USB
	)
	device.set_gpio_output(pin=13, level=1)  # switch on LED

Note: that individual pins and functions must be enabled and supported by the `Device`.

.. autoclass:: uosinterface.hardware.__init__.UOSDevice
	:members:

Hardware Interfaces
-------------------

*	Stub
*	USB Serial
