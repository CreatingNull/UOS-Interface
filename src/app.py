"""Root class for starting the daemon/webapp."""
from logging import DEBUG
from logging import getLogger as Log
from os import environ

from gevent.pywsgi import WSGIServer

from uosinterface import base_dir
from uosinterface import static_dir
from uosinterface.hardware import register_logs as register_hardware_logs
from uosinterface.util import configure_logs
from uosinterface.webapp import create_app
from uosinterface.webapp.dashboard import shutdown_server

__flask_debug = environ.get("FLASK_DEBUG", "false") == "true"
__host = environ.get("FLASK_HOST", "127.0.0.1")

app = create_app(__flask_debug, base_path=base_dir, static_path=static_dir)
register_hardware_logs(DEBUG, base_dir)
configure_logs("server", DEBUG, base_dir)

server = WSGIServer((__host, 5000), app, log=Log("server"))
server.start()
try:
    shutdown_server.wait()
except KeyboardInterrupt:
    pass  # allow exit via ctrl-C.
server.stop()
