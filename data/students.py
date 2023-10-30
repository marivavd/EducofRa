import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Student(SqlAlchemyBase, UserMixin):
    __tablename__ = 'students'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    id_user = sqlalchemy.Column(sqlalchemy.Integer)

    def __repr__(self):
        return f'<Student> {self.id} {self.name} {self.email}'

