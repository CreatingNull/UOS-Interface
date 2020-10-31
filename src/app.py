"""Root class for starting the daemon/webapp."""
import sys
from logging import DEBUG
from pathlib import Path

from uosinterface.hardware import register_logs as register_hardware_logs
from uosinterface.util import load_config
from uosinterface.webapp import create_app

base_dir = Path(__file__).resolve().parents[1]
conf = load_config(base_dir.joinpath(Path("resources/UARTOSInterface.ini")))
if conf is None or "Flask Config" not in conf:
    raise FileNotFoundError("App Config is missing or broken")
app = create_app(conf, base_path=base_dir)
register_hardware_logs(DEBUG, base_dir)


if __name__ == "__main__":
    if getattr(sys, "frozen", True):  # in deployment
        app.run(
            debug=conf.getboolean("App Config", "DEBUG"),
            host=conf["App Config"]["HOST"],
        )
    else:
        app.run(debug=True, host="127.0.0.1")
