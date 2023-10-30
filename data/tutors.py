import sqlalchemy
from flask_login import UserMixin


from .db_session import SqlAlchemyBase


class Tutor(SqlAlchemyBase, UserMixin):
    __tablename__ = 'tutors'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    id_user = sqlalchemy.Column(sqlalchemy.Integer)


    def __repr__(self):
        return f'<Tutor> {self.id} {self.name} {self.email}'

