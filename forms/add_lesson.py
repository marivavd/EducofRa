from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired


class LessonForm(FlaskForm):
    name = StringField('Назввние курса', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    status = StringField('Ваш статус', validators=[DataRequired()])
    phone_number = StringField('Номер телефона', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


    def get_public(self):
        return {'name': self.name.data,
                'surname': self.surname.data,
                'email': self.email.data,
                'phone_number': self.phone_number.data,
                'password': self.password.data,
                'status': self.status.data}
