from flask import request, jsonify, Blueprint

from data import db_session
from data.users import User
from data.db import MyDataBase

from random import choice
import json

blueprint = Blueprint('main_api', __name__, template_folder='templates')
db = MyDataBase()


@blueprint.route('/api/register/', methods=['GET'])
def register():
    user = User(
        name=request.args.get('name'),
        surname=request.args.get('surname'),
        email=request.args.get('email'),
        phone_number=request.args.get('phone_number'),
    )
    user.set_password(request.args.get('password'))
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()