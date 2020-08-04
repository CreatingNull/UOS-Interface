from pathlib import Path
import os
from UARTOSInterface import create_app, load_config


base_dir = Path(__file__).resolve().parent.parent
conf = load_config(base_dir.joinpath(Path("resources/UARTOSInterface.ini")))
if conf is None or "Flask Config" not in conf:
    raise FileNotFoundError("App Config is missing or broken")
app = create_app(conf, base_dir=base_dir)


if __name__ == "__main__":
    print("here")
    if os.environ.get("RUNNING_IN_CONTAINER", False):  # in deployment
        app.run(debug=conf.getboolean("App Config", "DEBUG"), host=conf["App Config"]["HOST"])
    else:
        app.run(debug=True, host="0.0.0.0")
