from data.tutors import Tutor
from data.students import Student
from data.parents import Parent
from data.users import User
from data import db_session


class MyDataBase:
    def __init__(self):
        db_session.global_init("tutorcoon.db")
        self.db_sess = db_session.create_session()

    def check_email_of_tutor(self, email):
        return self.db_sess.query(Tutor).filter(Tutor.email == email).first()

    def check_email_of_student(self, email):
        return self.db_sess.query(Student).filter(Student.email == email).first()

    def check_email_of_parent(self, email):
        return self.db_sess.query(Parent).filter(Parent.email == email).first()

