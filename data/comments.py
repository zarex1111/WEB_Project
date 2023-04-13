import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Comment(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'comments'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    task_id = sa.Column(sa.Integer, sa.ForeignKey('tasks.id'))
    author_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    text = sa.Column(sa.String)
    pseudonim = sa.Column(sa.String)