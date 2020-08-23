# ![NullTek Documentation](../resources/NullTekDocumentationLogo.png) Hardware Communication Layer

#### Scope: 
This document covers the structure and use of the UARTOSInterface hardware backend for direct communication with UOS devices.
The HardwareCOM package can be used as a standalone wrapper for UOS communication, or indirectly through the UARTOS WebApp dashboard interface. 

## Usage

Describe the wrapper interface

## Architecture

### Package Class
At a high level the HardwareCOM package contains the UOSDevice class that creates an communication instance to a single UOS device. 
##### Connection Creation:
The user instantiates this class with the identity (device type) and connection string. 
By default the UOSDevice object is 'lazy loaded' and no connection is made to the device until an explict operation function call is made. 
##### Function Calls
Supported function calls may be made to the UOS device through the applicable wrapper functions. 
Where applicable wrapper functions use a volatility constant in accordance with UOS. 
These constants should be imported directly from the package (*SUPER_VOLATILE*, *VOLATILE*, *NON_VOLATILE*). 

For addition technical details on UOS and low level device functions see [NullTek UART OS Documentation.](https://nulltek.xyz/wiki/doku.php?id=uart_aos)

* **set_gpio_output** - Used for digital IO writing functionality.
* **get_gpio_input** - Used for digital IO reading functionality. 
* **get_adc_input** - Used for analog IO reading functionality. 
* **reset_all_io** - Used for blanket system reset functionality. 

### Interfaces

* USB Serial Driver (UART)

Currently the only interface available for use on devices is UART via a USB converter. 
The system is designed to be interface agnostic so that further interfaces can be added in the future using the same wrapper. 