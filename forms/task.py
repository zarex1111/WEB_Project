from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class AddCourse(FlaskForm):
    title = StringField('Название *', validators=[DataRequired()])
    description = TextAreaField('Описание')
    is_login_required = BooleanField('Предоставить доступ неавторизованным пользователям?')
    submit = SubmitField('Создать')


class AddTask(FlaskForm):
    title = StringField('Название *', validators=[DataRequired()])
    condition = TextAreaField('Условие')
    submit = SubmitField('Создать')


class AddTest(FlaskForm):
    idata = TextAreaField('input')
    odata = TextAreaField('output')
    submit = SubmitField('Добавить')


class AddSolution(FlaskForm):
    code = TextAreaField('Код решения', validators=[DataRequired()])
    submit = SubmitField('Отправить')