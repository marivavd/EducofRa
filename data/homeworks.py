import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Homework(SqlAlchemyBase, UserMixin):
    __tablename__ = 'homeworks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.Date, nullable=True)
    done_homework_and_scores = sqlalchemy.Column(sqlalchemy.JSON, nullable=True, default={'done': [], 'scores': {}})

    def __repr__(self):
        return f'<Homework> {self.id}'
