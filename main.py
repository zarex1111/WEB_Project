from flask import Flask, render_template, request, redirect, abort
from base_config import base_config
import requests
from data.db_session import global_init, create_session
from data.__all_models import *
from forms.user import *
from forms.task import *
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
        return redirect(f'/login')
    return render_template('register.html', title="Регистрация", form=form, **base_config())


@app.route("/main")
@app.route("/")
def welcome_page():
    return render_template("main.html", title="DOODLE - проверь свой код!", **base_config())


@app.route('/profile')
def profile_page():
    if current_user.is_authenticated:
        data = current_user
        sess = create_session()
        if data:
            user_info = {
                'name': data.name,
                'surname': data.surname,
                'image': data.image,
                'courses': sess.query(Course).filter(Course.author_id == current_user.id),
                'tasks': [],
                'role': ('Учитель', 'Ученик')[data.role - 1],
                'email': data.email,
                'login': data.login
            }
            return render_template('profile.html', user_info=user_info, **base_config())
        

@app.route('/delete/<string:type>/<int:id>')
@login_required
def delete_smth(type, id):
    sess = create_session()
    if type == 'course':
        course = sess.query(Course).filter(Course.author_id == current_user.id, Course.id == id).first()
        if course:
            sess.delete(course)
            sess.commit()
            return redirect('/profile')
        else:
            abort(404)
    elif type == 'task':
        task = sess.query(Task).filter(Task.id == id, Task.author_id == current_user.id).first()
        if task:
            sess.delete(task)
            sess.commit()
            return redirect('/profile')
        else:
            abort(404)
    else:
        abort(404)


@app.route('/edit/course/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_course(id):
    sess = create_session()
    course = sess.query(Course).filter(Course.author_id == current_user.id, Course.id == id).first()
    if course:
        form = AddCourse()
        if request.method == 'GET':
            form.title.data = course.title
            form.description.data = course.description
            form.is_login_required.data = course.is_login_required
        if form.validate_on_submit():
            course.title = form.title.data
            course.description = form.description.data
            course.is_login_required = form.is_login_required.data
            sess.commit()
            return redirect('/profile')
        return render_template('add_course.html', **base_config(), title='Редактировать курс', form=form)
    

@app.route('/edit/task/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    sess = create_session()
    task = sess.query(Task).filter(Task.author_id == current_user.id).first()
    if task:
        form = AddTask()
        if request.method == 'GET':
            form.title.data = task.title
            form.condition.data = task.condition
        if form.validate_on_submit():
            task.title = form.title.data
            task.condition = form.condition.data
            sess.commit()
            return redirect('/course/' + str(task.course_id))
        return render_template('add_task.html', **base_config(), title='Редактировать задачу', form=form)



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


@app.route('/course/<int:id>')
def course_page(id):
    sess = create_session()
    course = sess.query(Course).filter(Course.id == id).first()
    if course:
        return render_template('course.html', **base_config(), title=course.title, course=course, tasks=sess.query(Task).filter(Task.course_id == id).all())
    
@app.route('/task/<int:id>')
def task_page(id):
    sess = create_session()
    task = sess.query(Task).filter(Task.id == id).first()
    if task:
        course = sess.query(Course).filter(Course.id == task.course_id).first()
        if course.is_login_required and not current_user.is_authenticated:
            abort(404)
        return render_template('task.html', **base_config(), title=task.title, task=task, tests=sess.query(Test).filter(Test.task_id == task.id).all())


@app.route('/add_course', methods=['GET', 'POST'])
@login_required
def add_course_page():
    form = AddCourse()
    if form.validate_on_submit():
        sess = create_session()
        course = Course()
        course.title = form.title.data
        course.description = form.description.data
        course.is_login_required = form.is_login_required.data
        course.author_id = current_user.id
        sess.add(course)
        sess.commit()
        return redirect('/profile')
    return render_template('add_course.html', title='Добавить курс', **base_config(), form=form)


@app.route('/add_task/<int:course_id>', methods=['GET', 'POST'])
@login_required
def add_task_page(course_id):
    form = AddTask()
    if not create_session().query(Course).filter(Course.id == course_id).first():
        return
    if form.validate_on_submit():
        sess = create_session()
        task = Task()
        task.title = form.title.data
        task.condition = form.condition.data
        task.course_id = course_id
        task.author_id = current_user.id
        sess.add(task)
        sess.commit()
        return redirect('/course/' + str(course_id))
    return render_template('add_task.html', title='Добавить задачу', **base_config(), form=form)


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