import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Student(SqlAlchemyBase, UserMixin):
    __tablename__ = 'students'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    id_user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('all_users.id'))
    tutors_and_parents_and_lessons = sqlalchemy.Column(sqlalchemy.JSON, nullable=True, default={"id_of_tutors": [],
                                                                       "id_of_lessons": [], "id_of_parents": []})

    def __repr__(self):
        return f'<Student> {self.id} {self.name}'

