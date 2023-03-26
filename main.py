from flask import Flask, render_template, request, redirect
from base_config import base_config
import requests
from data.db_session import global_init, create_session
from data.__all_models import *
from forms.user import *
from random import choices
from string import ascii_lowercase
from PIL import Image
import os
import email_api
from useful_tools import smart_split
from flask_login import LoginManager, login_user, current_user, login_required, logout_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_EXTENSIONS'] = ['jpg', 'png']

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    sess = create_session()
    return sess.query(User).get(user_id)


def main():
    global_init("db/database.db")
    app.register_blueprint(email_api.blueprint)
    app.run(port=8080, host='127.0.0.1')


@app.route("/base")
def main_page():
    return render_template("base.html", **base_config())


@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm(role=1)
    if form.validate_on_submit():
        sess = create_session()
        print('Форма обрабатывается')
        if sess.query(User).filter(User.email == form.email.data).first():
            return render_template("register.html", title="Регистрация", form=form,
                message="Пользователь с такой же почтой уже зарегистрирован", **base_config())
        if sess.query(User).filter(User.login == form.login.data).first():
            return render_template("register.html", title="Регистрация", form=form,
                message="Пользователь с таким же логином", **base_config())

        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            login=form.login.data,
            role=form.role.data,
        )

        file_data = request.files.get('image')
        if file_data:
            filetype = file_data.filename.split('.')[1]
            if filetype not in ('jpg', 'png'):
                return render_template("register.html", title="Регистрация", form=form,
                    message="Неверный тип файла", **base_config())
            new_filename = ''.join(choices(list(ascii_lowercase), k=10)) + '.jpg'
            print(new_filename)
            path = 'profile_pictures/' + new_filename
            file_data.save(path)
            user.image = path
        else:
            user.image = 'profile_pictures/basic.jpg'
            
        user.set_password(form.password.data)
        sess.add(user)
        sess.commit()
        return redirect(f'/profile/{sess.query(User).filter(User.login == user.login).first().id}')
    return render_template('register.html', title="Регистрация", form=form, **base_config())


@app.route("/main")
@app.route("/")
def welcome_page():
    return render_template("main.html", title="DOODLE - проверь свой код!", **base_config())


@app.route('/profile')
def profile_page():
    if current_user.is_authenticated:
        data = current_user
        if data:
            user_info = {
                'name': data.name,
                'surname': data.surname,
                'image': data.image,
                'courses': smart_split(data.courses, ' '),
                'tasks': smart_split(data.tasks, ' '),
                'role': ('Учитель', 'Ученик')[data.role - 1],
                'email': data.email,
                'login': data.login
            }
            return render_template('profile.html', user_info=user_info, **base_config())
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        sess = create_session()
        user = sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', message='Неправильный адрес электронной почты или пароль', form=form, title='Авторизация', **base_config())
    return render_template('login.html', form=form, title='Авторизация', **base_config())


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.errorhandler(404)
def err404(e):
    return "For some reason, that page doesn't exist"


@app.errorhandler(400)
def err400(e):
    return "Server cannot reach some data"


@app.errorhandler(500)
def err500(e):
    return "My code doesn't work as well, my bad"


if __name__ == '__main__':
    main()