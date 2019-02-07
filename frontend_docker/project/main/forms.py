from flask_wtf import FlaskForm as Form # depreciation correction
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
