import datetime
import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    surname = sa.Column(sa.String, index=True)
    name = sa.Column(sa.String)
    login = sa.Column(sa.String, index=True)
    email = sa.Column(sa.String, index=True)
    hashed_password = sa.Column(sa.String)
    role = sa.Column(sa.Integer, index=True)
    image = sa.Column(sa.String)
    courses = sa.Column(sa.String)
    tasks = sa.Column(sa.String)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)