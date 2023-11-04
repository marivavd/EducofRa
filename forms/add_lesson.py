from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired


class LessonForm(FlaskForm):
    name = StringField('Название курса', validators=[DataRequired()])
    weekday = StringField('Дни занятий', validators=[DataRequired()])
    submit = SubmitField('Добавить')


    def get_weekday(self):
        return self.weekday.data
