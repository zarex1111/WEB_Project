import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Solution(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'comments'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    task_id = sa.Column(sa.Integer, sa.ForeignKey('tasks.id'))
    code = sa.Column(sa.String)
    accuracy = sa.Column(sa.Integer)