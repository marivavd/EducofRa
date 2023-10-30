from data.users import User
from data import db_session


class MyDataBase:
    def __init__(self):
        db_session.global_init("tutorcoon.db")
        self.db_sess = db_session.create_session()

    def check_email(self, email):
        return self.db_sess.query(User).filter(User.email == email).first()

