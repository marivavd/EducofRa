from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    id = StringField('Введите id пользователя, которого вы хотите добавить', validators=[DataRequired()])
    submit = SubmitField('Добавить')

    def get_id(self):
        return int(self.id.data)
