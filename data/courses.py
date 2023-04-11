import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Course(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'courses'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String)
    description = sa.Column(sa.String, nullable=True)
    is_login_required = sa.Column(sa.Boolean)
    tasks = sa.Column(sa.String, nullable=True)
    author_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    user = orm.Relationship('User')