from flask import Flask, render_template, redirect, request, abort, url_for
from requests import get
from data import db_session
from flask_login import LoginManager, current_user, logout_user, login_required, login_user
from forms import parent, student, tutor
from data.tutors import Tutor
from data.db import MyDataBase

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db = MyDataBase()

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Tutor).get(user_id)


@app.route("/", methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:
        return render_template('index.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
