from flask import request, jsonify, Blueprint
from requests import post
from data import db_session
from data.users import User
from data.tutors import Tutor
from data.students import Student
from data.parents import Parent
from data.db import MyDataBase


blueprint = Blueprint('main_api', __name__, template_folder='templates')
db = MyDataBase()


@blueprint.route('/api/register/', methods=['POST'])
def register():
    status = request.args.get('status')
    user = User(
        name=request.args.get('name'),
        surname=request.args.get('surname'),
        email=request.args.get('email'),
        phone_number=request.args.get('phone_number'),
        status=request.args.get('status'),
        avatar=f'{status}.jpg'
    )
    email = user.email
    user.set_password(request.args.get('password'))
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()
    user = db_sess.query(User).filter(User.email == email).first()
    params = {'name': user.name, 'surname': user.surname, 'id_user': user.id}
    post('http://127.0.0.1:5000/api/register_tutor/', params=params) if user.status == 'tutor' else (
        post('http://127.0.0.1:5000/api/register_student/', params=params) if user.status == 'student' else post(
            'http://127.0.0.1:5000/api/register_parent/', params=params))
    return jsonify({'success': 'OK'})


@blueprint.route('/api/register_tutor/', methods=['POST'])
def register_tutor():
    tutor = Tutor(
        name=request.args.get('name'),
        surname=request.args.get('surname'),
        id_user=request.args.get('id_user')
    )
    db_sess = db_session.create_session()
    db_sess.add(tutor)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/register_student/', methods=['POST'])
def register_student():
    student = Student(
        name=request.args.get('name'),
        surname=request.args.get('surname'),
        id_user=request.args.get('id_user')
    )
    db_sess = db_session.create_session()
    db_sess.add(student)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/register_parent/', methods=['POST'])
def register_parent():
    parent = Parent(
        name=request.args.get('name'),
        surname=request.args.get('surname'),
        id_user=request.args.get('id_user')
    )
    db_sess = db_session.create_session()
    db_sess.add(parent)
    db_sess.commit()
    return jsonify({'success': 'OK'})
