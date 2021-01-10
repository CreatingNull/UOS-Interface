"""Module contains form class prototypes used in the web dashboard."""
from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import HiddenField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired
from wtforms.validators import NumberRange

# Ignore the min public methods check for form classes.
# pylint: disable=R0903


class ConnectDeviceForm(FlaskForm):
    """Form for posting a device connection request from the dashboard."""

    device_connection = HiddenField(
        id="form-device-connection", default=None, validators=[DataRequired()]
    )


class DigitalInstructionForm(FlaskForm):
    """For for posting a digital instruction from the dashboard."""

    device_connection = HiddenField(
        id="digital-form-device-connection", default=None, validators=[DataRequired()]
    )
    pin_index = IntegerField(
        id="pin-index", label="Pin Index", validators=[NumberRange(0, 255)]
    )
    pin_mode = BooleanField(id="pin-mode", default=False, label="Set Output")
    pin_level = BooleanField(id="pin-level", default=False, label="Set High")
