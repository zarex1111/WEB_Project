from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class AddCourse(FlaskForm):
    title = StringField('Название *', validators=[DataRequired()])
    description = TextAreaField('Описание')
    is_login_required = BooleanField('Предоставить доступ неавторизованным пользователям?')
    submit = SubmitField('Создать')