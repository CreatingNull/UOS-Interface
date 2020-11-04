"""Module contains form class prototypes used in the web dashboard."""
from flask_wtf import FlaskForm
from wtforms import HiddenField
from wtforms.validators import DataRequired


class ConnectDeviceForm(FlaskForm):
    """Form for posting a device connection request to the dashboard."""

    device_connection = HiddenField(
        id="form-device-connection", default=None, validators=[DataRequired()]
    )
