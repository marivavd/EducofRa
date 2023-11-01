from flask import Flask, render_template, redirect, request, abort, url_for
from data import db_session
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, current_user, logout_user, login_required, login_user
from api import main_api
from data.users import User
from requests import get, put, post
from data.db import MyDataBase
from datetime import date
import calendar


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
    current_date = str(date.today()).split('-')
    year, month = int(current_date[0]), int(current_date[1])
    cort = calendar.monthrange(year, month)
    if cort[0] == 0:
        sp_before = []
    else:
        month_before = month - 1
        if month_before == 0:
            month_before = 12
            cort_before = calendar.monthrange(year - 1, month_before)
        else:
            cort_before = calendar.monthrange(year, month_before)
        sp = [i for i in range(cort_before[1] + 1)]
        sp_before = [i for i in sp[-1 * cort[0]:]]
    sp_now = []
    a = 1
    while a < cort[1]:
        if a == 1:
            sp_now.append([i for i in range(1, 7 - cort[0] + 1)])
            a = sp_now[0][-1]
        elif a + 7 <= cort[1]:
            sp_now.append([i for i in range(sp_now[-1][-1] + 1, sp_now[-1][-1] + 8)])
            a = sp_now[-1][-1]
        else:
            sp_now.append([i for i in range(sp_now[-1][-1] + 1, cort[1] + 1)])
            a = sp_now[-1][-1]
    sp_after = []
    print(cort)
    for i in range(1, 7 - len(sp_now[-1]) + 1):
        sp_after.append(i)
    if len(sp_after) == 7:
        sp_after = []
    if len(sp_now) == 5:
        height = 550
    else:
        height = 600
    sp_week = ['Понедельник', 'Вторник', "Среда", "Четверг", "Пятница", "Суббота", "Восресенье"]
    return render_template("home.html", sp_before=sp_before, sp_now=sp_now, sp_after=sp_after, height=height,
                           week_day=sp_week[cort[0]], number=12, month=month, year=year)


if __name__ == '__main__':
    db_session.global_init("tutorcoon.db")
    app.register_blueprint(main_api.blueprint)
    app.run(port=5000, host='127.0.0.1')
