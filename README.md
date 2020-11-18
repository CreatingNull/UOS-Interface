# ![NullTek Documentation](resources/NullTekDocumentationLogo.png) UART OS Interface

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](LICENSE.md) 
[![Codacy Inspection](https://app.codacy.com/project/badge/Grade/4d0be714379a46bca8b1a62d706d150b)](https://www.codacy.com/manual/CreatingNull/UART-Operating-System-Interface/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=CreatingNull/UART-Operating-System-Interface&amp;utm_campaign=Badge_Grade)
[![Codacy Coverage](https://app.codacy.com/project/badge/Coverage/8a24020489ee4638aa10449e3f1cc0cd)](https://www.codacy.com/gh/CreatingNull/UART-Operating-System-Interface/dashboard?utm_source=github.com&utm_medium=referral&utm_content=CreatingNull/UART-Operating-System-Interface&utm_campaign=Badge_Coverage)
[![Build Status](https://travis-ci.org/CreatingNull/UART-Operating-System-Interface.svg?branch=master)](https://travis-ci.org/CreatingNull/UART-Operating-System-Interface)

Python Interface for remote communication and control of a UOS Compliant Microcontroller.

Status: Still under development, not ready for a release yet. 

---

## Contributing

If this project ever gets to any sort of usable state, it would be great to get any community additions. 

### Dependencies

The project backend is written using Python Flask.
Backend requirements can be found in [requirements.txt](resources/requirements.txt).

```pip install -r resources/requirements.txt```

The project front end is vanilla javascript, html and css. 
Frontend requirements:
*   FontAwesome 5.14.0 - for development this should be nested in `src/uosinterface/webapp/static/lib/FontAwesome`

### Code Formatting

This project uses:

*   Black / reorder-python-imports for Python Formatting

    ``` pip install black ```
    
    ``` pip install reorder-python-imports ```

*   Docformatter for Python Docstring formatting

    ``` pip install docformatter ```
    
    ``` docformatter --in-place --blank --pre-summary-newline ```

*   Prettier for js/html/css formatting

    ``` npm install --save-dev --save-exact prettier ```

To make life easy these should be hooked on commits or just run a 'on save' file-watcher.

## Donations

I just do this stuff for fun, but if you found any of my work helpful a little tip would be very much appreciated. 

[![Support via buymeacoffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/nulltek)

---

## License

The source of this repo uses the MIT open-source license, for details on the current licensing see LICENSE.md or click the badge above. 
*   Copyright 2020 © <a href="https://nulltek.xyz" target="_blank">NullTek</a>.
