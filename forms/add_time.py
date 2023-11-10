from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField
from wtforms_alchemy import QuerySelectMultipleField
from wtforms.validators import DataRequired


class TimeForm(FlaskForm):
    weekday = StringField(validators=[DataRequired()])
    weekday_time = TimeField(validators=[DataRequired()])

    def get_time(self):
        return self.weekday_time.data

