from flask_wtf import FlaskForm
from wtforms import FieldList, SubmitField, FormField
from .add_time import TimeForm


class Listform(FlaskForm):
    list_time = FieldList(FormField(TimeForm))
    submit = SubmitField('Добавить')

