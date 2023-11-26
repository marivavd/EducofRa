import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm


from .db_session import SqlAlchemyBase


class Video_lesson(SqlAlchemyBase, UserMixin):
    __tablename__ = 'video_lessons'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    link = sqlalchemy.Column(sqlalchemy.String, nullable=True)



    def __repr__(self):
        return f'<Video_lesson> {self.id} {self.name}'
