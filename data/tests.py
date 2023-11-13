import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm


from .db_session import SqlAlchemyBase


class Test(SqlAlchemyBase, UserMixin):
    __tablename__ = 'tests'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    link = sqlalchemy.Column(sqlalchemy.String, nullable=True)



    def __repr__(self):
        return f'<Lesson> {self.id} {self.name}'
