import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


class Parent(SqlAlchemyBase, UserMixin):
    __tablename__ = 'parents'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    id_user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('all_users.id'))
    id_of_children = sqlalchemy.Column(sqlalchemy.JSON, nullable=True, default={"id_of_children": []})

    def __repr__(self):
        return f'<Parent> {self.id} {self.name}'

