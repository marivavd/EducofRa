import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Lesson(SqlAlchemyBase, UserMixin):
    __tablename__ = 'lessons'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    id_tutor = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tutors.id_user'))
    students_and_when = sqlalchemy.Column(sqlalchemy.JSON, nullable=True, default={"id_of_students": [],
                                                                                   "when": []})
    homeworks = sqlalchemy.Column(sqlalchemy.JSON, nullable=True, default={})
    scores = sqlalchemy.Column(sqlalchemy.JSON, nullable=True, default={})

    def __repr__(self):
        return f'<Lesson> {self.id} {self.name}'
