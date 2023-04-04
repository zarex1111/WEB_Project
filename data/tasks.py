import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Task(SqlAlchemyBase):
    __tablename__ = 'tasks'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    course_id = sa.Column(sa.Integer, sa.ForeignKey('courses.id'))
    author_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    title = sa.Column(sa.String)
    condition = sa.Column(sa.String)
    user = orm.relationship('User')