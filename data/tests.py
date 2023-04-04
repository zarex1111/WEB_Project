import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Test(SqlAlchemyBase):
    __tablename__ = 'tests'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    task_id = sa.Column(sa.Integer, sa.ForeignKey('tasks.id'))
    idata = sa.Column(sa.String)
    odata = sa.Column(sa.String)
    task = orm.relationship('Task')