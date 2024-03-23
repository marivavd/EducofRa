import sqlalchemy
from flask_login import UserMixin


from .db_session import SqlAlchemyBase


class Help_material(SqlAlchemyBase, UserMixin):
    __tablename__ = 'help_materials'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    link = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    grade = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    subject = sqlalchemy.Column(sqlalchemy.String, nullable=True)



    def __repr__(self):
        return f'<Help_material> {self.id} {self.name}'
