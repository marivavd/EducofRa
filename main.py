from flask import Flask, render_template, redirect, request, abort, url_for
from data import db_session
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, current_user, logout_user, login_required, login_user
from api import main_api
from data.users import User
from requests import get, put, post
from data.db import MyDataBase

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db = MyDataBase()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if not form.validate_on_submit():
        return render_template('register.html', title='Регистрация', form=form)

    db_sess = db_session.create_session()
    if not form.check_password_again():
        return render_template('register.html', title='Регистрация', form=form,
                               message="Пароли не совпадают")
    elif db_sess.query(User).filter(User.email == form.email.data).first():
        return render_template('register.html', title='Регистрация', form=form,
                               message="Такой пользователь уже есть")
    else:
        post('http://127.0.0.1:5000/api/register/', params=form.get_public())
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/", methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:
        return render_template('index.html')
    print(1)

    return render_template("home.html")


if __name__ == '__main__':
    db_session.global_init("tutorcoon.db")
    app.register_blueprint(main_api.blueprint)
    app.run(port=5000, host='127.0.0.1')
