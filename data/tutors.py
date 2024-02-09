import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm


from .db_session import SqlAlchemyBase


class Tutor(SqlAlchemyBase, UserMixin):
    __tablename__ = 'tutors'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    id_user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('all_users.id'))
    subjects = sqlalchemy.Column(sqlalchemy.JSON, nullable=True, default={"subjects": []})
    students_and_lessons = sqlalchemy.Column(sqlalchemy.JSON, nullable=True, default={"id_of_students": [],
                                                                       "id_of_lessons": []})
    about = sqlalchemy.Column(sqlalchemy.Text)
    summa_marks = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    count_marks = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    reviews = sqlalchemy.Column(sqlalchemy.JSON, default={})
    lessons = orm.relationship("Lesson", backref='tutors')


    def __repr__(self):
        return f'<Tutor> {self.id} {self.name}'

