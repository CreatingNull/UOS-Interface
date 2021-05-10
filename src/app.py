"""Root class for starting the daemon/webapp."""
import sys
from logging import DEBUG
from os import environ

from uosinterface import base_dir
from uosinterface import static_dir
from uosinterface.hardware import register_logs as register_hardware_logs
from uosinterface.webapp import create_app

__flask_debug = environ.get("FLASK_DEBUG", "false") == "true"
app = create_app(__flask_debug, base_path=base_dir, static_path=static_dir)
register_hardware_logs(DEBUG, base_dir)


if __name__ == "__main__":
    __host = environ.get("FLASK_HOST", "127.0.0.1")
    if getattr(sys, "frozen", False):  # in deployment
        app.run(debug=__flask_debug, host=__host)
    else:
        app.run(debug=True, host=__host)
