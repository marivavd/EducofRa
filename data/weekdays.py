import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Weekday(SqlAlchemyBase, UserMixin):
    __tablename__ = 'weekdays'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __str__(self):
        return self.name
