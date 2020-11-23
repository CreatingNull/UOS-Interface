"""Root class for starting the daemon/webapp."""
import sys
from logging import DEBUG
from os import environ
from pathlib import Path

from uosinterface.hardware import register_logs as register_hardware_logs
from uosinterface.webapp import create_app

if getattr(sys, "frozen", False):  # in deployment
    base_dir = Path(sys.executable).parent
    static_dir = base_dir.joinpath("static/")
else:  # development
    base_dir = Path(__file__).parents[1]
    static_dir = base_dir.joinpath("src/uosinterface/webapp/static/")
__flask_debug = environ.get("FLASK_DEBUG", "false") == "true"
app = create_app(__flask_debug, base_path=base_dir, static_path=static_dir)
register_hardware_logs(DEBUG, base_dir)


if __name__ == "__main__":
    __host = environ.get("FLASK_HOST", "127.0.0.1")
    if getattr(sys, "frozen", False):  # in deployment
        app.run(debug=__flask_debug, host=__host)
    else:
        app.run(debug=True, host=__host)
