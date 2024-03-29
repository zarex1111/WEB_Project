from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, SelectField, FileField, BooleanField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('Имя и фамилия *', validators=[DataRequired()])
    surname = StringField(validators=[DataRequired()])
    login = StringField('Логин *', validators=[DataRequired()])
    email = EmailField('e-mail *', validators=[DataRequired()])
    role = SelectField('Ученик или учитель? *', validators=[DataRequired()], choices=[(1, 'Учитель'), (2, 'Ученик')])
    password = PasswordField('Пароль *', validators=[DataRequired()])
    image = FileField('Выберите фото профиля (jpg, png)')
    submit = SubmitField('Авторизоваться')


class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')