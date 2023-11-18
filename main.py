import datetime

from flask import Flask, render_template, redirect, request, abort, url_for
from data import db_session
from forms.user import RegisterForm, LoginForm
from forms.adding import PostForm
from forms.add_lesson import LessonForm
from forms.list import Listform
from flask_login import LoginManager, current_user, logout_user, login_required, login_user
from api import main_api
from data.users import User
from data.tutors import Tutor
from data.weekdays import Weekday
from data.students import Student
from data.parents import Parent
from data.lessons import Lesson
from data.homeworks import Homework
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


@app.route("/day/<int:number>")
def day(number):
    current_month, current_year = datetime.datetime.today().month, datetime.datetime.today().year
    our_weekday = datetime.datetime(current_year, current_month, number).weekday()
    this_day = str(datetime.datetime(current_year, current_month, number).date())
    db_sess = db_session.create_session()
    sp_all = []
    if current_user.status == 'student':
        student = db_sess.query(Student).filter(Student.id_user == current_user.id).first()
        sp_lessons = student.tutors_and_parents_and_lessons['id_of_lessons']
        for id in sp_lessons:
            lesson = db_sess.query(Lesson).get(id)
            sp_dates = lesson.students_and_when['when']
            for i in sp_dates:
                if our_weekday == i[0]:
                    sp_all.append(i[1])
                    tutor = db_sess.query(User).get(lesson.id_tutor)
                    sp_all.append(f'{tutor.surname} {tutor.name}')
                    sp_all.append(lesson.name)
                    if this_day in lesson.homeworks.keys():
                        sp_all.append('+')
                    else:
                        sp_all.append('-')
                    sp_all.append(lesson.id)
        return render_template("day.html", who="Преподаватель", len_sp=len(sp_all), sp_all=sp_all, this_day=this_day)
    elif current_user.status == 'tutor':
        tutor = db_sess.query(Tutor).filter(Tutor.id_user == current_user.id).first()
        sp_lessons = tutor.students_and_lessons['id_of_lessons']
        for id in sp_lessons:
            lesson = db_sess.query(Lesson).get(id)
            sp_dates = lesson.students_and_when['when']
            for i in sp_dates:
                if our_weekday == i[0]:
                    sp_all.append(i[1])
                    students_id = lesson.students_and_when['id_of_students']
                    sp_students = []
                    for st_id in students_id:
                        student = db_sess.query(User).get(st_id)
                        sp_students.append(f'{student.surname} {student.name}')
                    sp_all.append(','.join(sp_students))
                    sp_all.append(lesson.name)
                    if this_day in lesson.homeworks.keys():
                        sp_all.append('+')
                    else:
                        sp_all.append('-')
                    sp_all.append(lesson.id)
        return render_template("day.html", who="Ученики", len_sp=len(sp_all), sp_all=sp_all, this_day=this_day)
    else:
        parent = db_sess.query(Parent).filter(Parent.id_user == current_user.id).first()
        for child_id in parent.id_of_children['id_of_children']:
            student = db_sess.query(Student).filter(Student.id_user == child_id).first()
            sp_lessons = student.tutors_and_parents_and_lessons['id_of_lessons']
            for id in sp_lessons:
                lesson = db_sess.query(Lesson).get(id)
                sp_dates = lesson.students_and_when['when']
                for i in sp_dates:
                    if our_weekday == i[0]:
                        sp_all.append(i[1])
                        sp_all.append(f'{student.surname} {student.name}')
                        sp_all.append(lesson.name)
                        if this_day in lesson.homeworks.keys():
                            sp_all.append('+')
                        else:
                            sp_all.append('-')
                        sp_all.append(lesson.id)
        return render_template("day.html", who="Ребёнок", len_sp=len(sp_all), sp_all=sp_all, this_day=this_day)


@app.route("/add_student", methods=['GET', 'POST'])
def add_student():
    form = PostForm()

    if request.method == 'GET':
        return render_template('adding.html', form=form)
    if not form.validate_on_submit():
        return render_template("adding.html", form=form)
    db_sess = db_session.create_session()
    if db_sess.query(Student).filter(Student.id_user == form.get_id()).first() != None:
        tutor = db_sess.query(Tutor).filter(Tutor.id_user == current_user.id).first()
        tutor.students_and_lessons["id_of_students"].append(form.get_id())
        put(f'http://127.0.0.1:5000/api/add_student/{current_user.id}',
            json={"students_and_lessons": tutor.students_and_lessons}).json()
        student = db_sess.query(Student).filter(Student.id_user == form.get_id()).first()
        student.tutors_and_parents_and_lessons["id_of_tutors"].append(current_user.id)
        put(f'http://127.0.0.1:5000/api/add_tutor_or_parent_or_lesson/{form.get_id()}',
            json={"tutors_and_parents_and_lessons": student.tutors_and_parents_and_lessons}).json()
    return redirect(f'/my_students/{current_user.id}')


@app.route("/add_tutor", methods=['GET', 'POST'])
def add_tutor():
    form = PostForm()

    if request.method == 'GET':
        return render_template('adding.html', form=form)
    if not form.validate_on_submit():
        return render_template("adding.html", form=form)
    db_sess = db_session.create_session()
    if db_sess.query(Tutor).filter(Tutor.id_user == form.get_id()).first() != None:
        tutor = db_sess.query(Tutor).filter(Tutor.id_user == form.get_id()).first()
        tutor.students_and_lessons["id_of_students"].append(current_user.id)
        put(f'http://127.0.0.1:5000/api/add_student/{form.get_id()}',
            json={"students_and_lessons": tutor.students_and_lessons}).json()
        student = db_sess.query(Student).filter(Student.id_user == current_user.id).first()
        student.tutors_and_parents_and_lessons["id_of_tutors"].append(form.get_id())
        put(f'http://127.0.0.1:5000/api/add_tutor_or_parent_or_lesson/{current_user.id}',
            json={"tutors_and_parents_and_lessons": student.tutors_and_parents_and_lessons}).json()
    return redirect(f'/my_tutors/{current_user.id}')


@app.route("/add_parent", methods=['GET', 'POST'])
def add_parent():
    form = PostForm()

    if request.method == 'GET':
        return render_template('adding.html', form=form)
    if not form.validate_on_submit():
        return render_template("adding.html", form=form)
    db_sess = db_session.create_session()
    if db_sess.query(Parent).filter(Parent.id_user == form.get_id()).first() != None:
        parent = db_sess.query(Parent).filter(Parent.id_user == form.get_id()).first()
        parent.id_of_children["id_of_children"].append(current_user.id)
        put(f'http://127.0.0.1:5000/api/add_child/{form.get_id()}',
            json={"id_of_children": parent.id_of_children}).json()
        student = db_sess.query(Student).filter(Student.id_user == current_user.id).first()
        student.tutors_and_parents_and_lessons["id_of_parents"].append(form.get_id())
        put(f'http://127.0.0.1:5000/api/add_tutor_or_parent_or_lesson/{current_user.id}',
            json={"tutors_and_parents_and_lessons": student.tutors_and_parents_and_lessons}).json()
    return redirect(f'/my_parents/{current_user.id}')


@app.route("/add_child", methods=['GET', 'POST'])
def add_child():
    form = PostForm()

    if request.method == 'GET':
        return render_template('adding.html', form=form)
    if not form.validate_on_submit():
        return render_template("adding.html", form=form)
    db_sess = db_session.create_session()
    if db_sess.query(Student).filter(Student.id_user == form.get_id()).first() != None:
        parent = db_sess.query(Parent).filter(Parent.id_user == current_user.id).first()
        parent.id_of_children["id_of_children"].append(form.get_id())
        put(f'http://127.0.0.1:5000/api/add_child/{current_user.id}',
            json={"id_of_children": parent.id_of_children}).json()
        student = db_sess.query(Student).filter(Student.id_user == form.get_id()).first()
        student.tutors_and_parents_and_lessons["id_of_parents"].append(current_user.id)
        put(f'http://127.0.0.1:5000/api/add_tutor_parent/{form.get_id()}',
            json={"tutors_and_parents_and_lessons": student.tutors_and_parents_and_lessons}).json()
    return redirect(f'/my_children/{current_user.id}')


@app.route("/add_course", methods=['GET', 'POST'])
def add_course():
    form = LessonForm()
    db_sess = db_session.create_session()
    form.weekday.query = db_sess.query(Weekday).all()
    if request.method == 'GET':
        return render_template('add_course.html', form=form)
    if not form.validate_on_submit():
        return render_template("add_course.html", form=form)
    line_sp = ','.join([i.name for i in form.get_all()['weekday']])
    return redirect(f"/choose_time/{form.get_all()['name']}/{line_sp}")


@app.route("/choose_time/<name>/<line_sp>", methods=['GET', 'POST'])
def choose_time(name, line_sp):
    weekday = [i for i in line_sp.split(',')]
    list_form = Listform(request.form)
    list_form.list_time.min_entries = len(weekday)
    for i in range(len(weekday)):
        list_form.list_time.append_entry()
    for i in range(len(list_form.list_time)):
        try:
            list_form.list_time[i].weekday = weekday[i]
        except Exception:
            db_sess = db_session.create_session()
            sl = {"id_of_students": [], "when": []}
            sl_week = {'Понедельник': 0, 'Вторник': 1, "Среда": 2, "Четверг": 3, "Пятница": 4, "Суббота": 5,
                       "Воскресенье": 6}
            for day in range(len(weekday)):
                sl['when'].append([sl_week[weekday[day]], str(list_form.list_time[day].get_time())])
            answer = post(f'http://127.0.0.1:5000/api/add_lesson/{current_user.id}', params={'name': name})
            lesson = db_sess.query(Lesson).filter(Lesson.id == answer.json()['id']).first()
            lesson.students_and_when["when"] = sl['when']
            put(f'http://127.0.0.1:5000/api/add_time/{lesson.id}',
                json={"students_and_when": lesson.students_and_when}).json()
            return redirect(f'/add_lesson_id_tutor/{answer.json()["id"]}')
    if request.method == 'GET':
        return render_template('choose_time.html', form=list_form, weekday=weekday)
    if not list_form.validate_on_submit():
        return render_template("choose_time.html", form=list_form, weekday=weekday)


@app.route("/add_lesson_id_tutor/<int:lesson_id>", methods=['GET', 'POST'])
def add_lesson_id_tutor(lesson_id):
    db_sess = db_session.create_session()
    if db_sess.query(Tutor).filter(Tutor.id_user == current_user.id).first() != None:
        tutor = db_sess.query(Tutor).filter(Tutor.id_user == current_user.id).first()
        tutor.students_and_lessons["id_of_lessons"].append(lesson_id)
        put(f'http://127.0.0.1:5000/api/add_lesson_for_tutor/{current_user.id}',
            json={"students_and_lessons": tutor.students_and_lessons}).json()
    return redirect('/')


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


@app.route("/my_students/<int:user_id>")
def my_students(user_id):
    db_sess = db_session.create_session()
    tutor = db_sess.query(Tutor).filter(Tutor.id_user == user_id).first()
    sp_id_of_students = tutor.students_and_lessons["id_of_students"]
    sp_students = []
    for i in sp_id_of_students:
        sp_students.append(db_sess.query(User).filter(User.id == i).first())
    return render_template("my.html", sp=sp_students, add_smth='add_student')


@app.route("/my_tutors/<int:user_id>")
def my_tutors(user_id):
    db_sess = db_session.create_session()
    student = db_sess.query(Student).filter(Student.id_user == user_id).first()
    sp_id_of_tutors = student.tutors_and_parents_and_lessons["id_of_tutors"]
    sp_tutors = []
    for i in sp_id_of_tutors:
        sp_tutors.append(db_sess.query(User).filter(User.id == i).first())
    return render_template("my.html", sp=sp_tutors, add_smth='add_tutor')


@app.route("/my_parents/<int:user_id>")
def my_parents(user_id):
    db_sess = db_session.create_session()
    student = db_sess.query(Student).filter(Student.id_user == user_id).first()
    sp_id_of_parents = student.tutors_and_parents_and_lessons["id_of_parents"]
    sp_parents = []
    for i in sp_id_of_parents:
        sp_parents.append(db_sess.query(User).filter(User.id == i).first())
    return render_template("my.html", sp=sp_parents, add_smth='add_parent')


@app.route("/my_children/<int:user_id>")
def my_children(user_id):
    db_sess = db_session.create_session()
    parent = db_sess.query(Parent).filter(Parent.id_user == user_id).first()
    sp_id_of_children = parent.id_of_children["id_of_children"]
    sp_children = []
    for i in sp_id_of_children:
        sp_children.append(db_sess.query(User).filter(User.id == i).first())
    return render_template("my.html", sp=sp_children, add_smth='add_child')


@app.route("/my_courses/<int:user_id>")
def my_courses(user_id):
    db_sess = db_session.create_session()
    if current_user.status == 'tutor':
        tutor = db_sess.query(Tutor).filter(Tutor.id_user == user_id).first()
        sp_id_of_lessons = tutor.students_and_lessons["id_of_lessons"]
    else:
        student = db_sess.query(Student).filter(Student.id_user == user_id).first()
        sp_id_of_lessons = student.tutors_and_parents_and_lessons["id_of_lessons"]
    sp_lessons = []
    for i in sp_id_of_lessons:
        sp_lessons.append(db_sess.query(Lesson).filter(Lesson.id == i).first())
    return render_template("my_courses.html", sp=sp_lessons, len_sp=len(sp_lessons))


@app.route("/course/<int:lesson_id>")
def course(lesson_id):
    db_sess = db_session.create_session()
    lesson = db_sess.query(Lesson).filter(Lesson.id == lesson_id).first()
    if current_user.status == 'tutor':
        sp_id_of_students_already = lesson.students_and_when['id_of_students']
        tutor = db_sess.query(Tutor).filter(Tutor.id_user == current_user.id).first()
        sp_stud_id = tutor.students_and_lessons['id_of_students']
        sp_stud = []
        for i in sp_stud_id:
            sp_stud.append(db_sess.query(Student).filter(Student.id_user == i).first())
        return render_template("course_for_tutor.html", lesson=lesson, sp_stud=sp_stud,
                               sp_id_of_students_already=sp_id_of_students_already)
    if current_user.status == 'student':
        tutor = db_sess.query(Tutor).filter(Tutor.id_user == lesson.id_tutor).first()
        return render_template("course_for_student.html", lesson=lesson, tutor=tutor)


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
    for i in range(1, 7 - len(sp_now[-1]) + 1):
        sp_after.append(i)
    if len(sp_after) == 7:
        sp_after = []
    if len(sp_now) == 5:
        height = 550
    else:
        height = 600
    sp_week = ['Понедельник', 'Вторник', "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    sl_months = {1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь', 7: 'Июль',
                 8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'}
    number = int(current_date[2] if current_date[2][0] != '0' else (current_date[2][1]))
    return render_template("home.html", sp_before=sp_before, sp_now=sp_now, sp_after=sp_after, height=height,
                           week_day=sp_week[cort[0]], number=number, month=sl_months[month], year=year)


@app.route("/user_page")
def user_page():
    if current_user.is_authenticated:
        if current_user.status == 'tutor':
            db_sess = db_session.create_session()
            tutor = db_sess.query(Tutor).filter(Tutor.id_user == current_user.id).first()
            return render_template("user_page.html",
                                   about=(tutor.about if tutor.about != None else ('Пока здесь ничего нет')))
        return render_template("user_page.html")


@app.route("/rewrite_info_for_tutor", methods=['GET', 'POST'])
def add_info():
    if request.method == 'POST':
        about = request.form['about']
        put(f'http://127.0.0.1:5000/api/rewrite_info_for_tutor/{current_user.id}', json={"about": about}).json()
        return redirect('/user_page')
    db_sess = db_session.create_session()
    tutor = db_sess.query(Tutor).filter(Tutor.id_user == current_user.id).first()
    return render_template("rewrite_info_for_tutor.html", about=(tutor.about if tutor.about != None else ('')))


@app.route("/add_homework/<date>/<int:lesson_id>", methods=['GET', 'POST'])
def add_homework(date, lesson_id):
    if request.method == 'POST':
        answer = post(f'http://127.0.0.1:5000/api/add_homework',
             json={'text': request.form['homework'], 'date': date}).json()
        db_sess = db_session.create_session()
        lesson = db_sess.query(Lesson).filter(Lesson.id == lesson_id).first()
        lesson.homeworks[date] = db_sess.query(Homework).filter(Homework.id == answer['id']).first().id
        put(f'http://127.0.0.1:5000/api/add_homework_in_lesson/{lesson.id}',
            json={'homeworks': lesson.homeworks}).json()
        return redirect(f'/day/{int(list(map(int, date.split("-")))[2])}')
    return render_template("add_homework.html", date=date, lesson_id=lesson_id)


@app.route("/watch_homework/<date>/<int:lesson_id>")
def watch_homework(date, lesson_id):
    db_sess = db_session.create_session()
    lesson = db_sess.query(Lesson).filter(Lesson.id == lesson_id).first()
    homework = db_sess.query(Homework).filter(Homework.id == lesson.homeworks[date]).first()
    text = homework.text
    if current_user.status == 'student':
        done = False
        if current_user.id in homework.done_homework_and_scores['done']:
            done = True
        return render_template('watch_homework_for_student.html', text=text, date=date, done=done, homework_id=homework.id)

@app.route("/change_status_of_homework/<int:homework_id>", methods=['GET', 'POST'])
def change_status_of_homework(homework_id):
    if request.method == 'POST':
        status = request.form['status']
        print(status)


@app.route("/show_page_of_user/<int:id_of_person>")
def show_page_of_user(id_of_person):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id_of_person).first()
    if user.status == 'tutor':
        tutor = db_sess.query(Tutor).filter(Tutor.id_user == id_of_person).first()
        if tutor.count_marks == 0:
            stars = 0
        else:
            stars = round(tutor.summa_marks / tutor.count_marks)
        return render_template("page_of_tutor.html", tutor=tutor, sl_reviews=tutor.reviews, stars=stars)
    elif user.status == 'student' and current_user.status == 'tutor':
        student = db_sess.query(Student).filter(Student.id_user == id_of_person).first()
        return render_template("page_of_student_for_tutor.html", student=student)


@app.route("/send_marks_for_tutor/<int:tutor_id>", methods=['GET', 'POST'])
def send_marks_for_tutor(tutor_id):
    if request.method == 'POST':
        mark = request.form['mark']
        db_sess = db_session.create_session()
        tutor = db_sess.query(Tutor).filter(Tutor.id_user == tutor_id).first()
        tutor.summa_marks += int(mark)
        tutor.count_marks += 1
        db_sess.commit()
    return redirect(f'/show_page_of_user/{tutor_id}')


@app.route("/send_reviews_for_tutor/<int:tutor_id>", methods=['GET', 'POST'])
def send_reviews_for_tutor(tutor_id):
    if request.method == 'POST':
        message = request.form['user_message']
        db_sess = db_session.create_session()
        tutor = db_sess.query(Tutor).filter(Tutor.id_user == tutor_id).first()
        tutor.reviews[f'{current_user.name} {current_user.surname}'] = message
        put(f'http://127.0.0.1:5000/api/comment_for_tutor/{tutor.id}',
            json={'reviews': tutor.reviews}).json()
    return redirect(f'/show_page_of_user/{tutor_id}')


@app.route("/change_students/<int:lesson_id>", methods=['GET', 'POST'])
def change_students(lesson_id):
    if request.method == 'POST':
        db_sess = db_session.create_session()
        tutor = db_sess.query(Tutor).filter(Tutor.id_user == current_user.id).first()
        sp = tutor.students_and_lessons["id_of_students"]
        sp_new_stud = []
        for i in sp:
            option1 = request.form.get(f'{i}')
            if option1:
                sp_new_stud.append(i)
                student = db_sess.query(Student).filter(Student.id_user == i).first()
                if lesson_id not in student.tutors_and_parents_and_lessons['id_of_lessons']:
                    student.tutors_and_parents_and_lessons['id_of_lessons'].append(lesson_id)
                    put(f'http://127.0.0.1:5000/api/add_tutor_or_parent_or_lesson/{student.id_user}',
                        json={"tutors_and_parents_and_lessons": student.tutors_and_parents_and_lessons}).json()
        lesson = db_sess.query(Lesson).filter(Lesson.id == lesson_id).first()
        lesson.students_and_when['id_of_students'] = sp_new_stud
        put(f'http://127.0.0.1:5000/api/change_students_in_lesson/{lesson.id}',
            json={"students_and_when": lesson.students_and_when}).json()
    return redirect(f'/course/{lesson_id}')


if __name__ == '__main__':
    db_session.global_init("tutorcoon.db")
    app.register_blueprint(main_api.blueprint)
    app.run(port=5000, host='127.0.0.1')
