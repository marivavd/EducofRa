from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms_alchemy import QuerySelectMultipleField
from wtforms.validators import DataRequired


class LessonForm(FlaskForm):
    name = StringField('Название курса', validators=[DataRequired()])
    weekday = QuerySelectMultipleField('Дни занятий', validators=[DataRequired()])
    submit = SubmitField('Добавить')


    def get_all(self):
        return {'weekday': self.weekday.data,
                'name': self.name.data}
