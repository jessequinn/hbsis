from flask_wtf import Form
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired


class WeatherRegistrationForm(Form):
    city = StringField(
        'city',
        validators=[DataRequired()]
    )
    country = SelectField(
        'country',
        coerce=str,
        validators=[DataRequired()]
    )
