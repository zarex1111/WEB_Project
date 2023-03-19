from flask import Flask, render_template, request
from base_config import base_config
import requests

app = Flask(__name__)

@app.route("/base")
def main_page():
    return render_template("base.html", **base_config())


@app.route("/register")
def register_page():
    if request.method == "GET":
        return render_template("register.html", title="Авторизация", **base_config())
    elif request.method=='POST':
        return "<h1>Good</h1>"

@app.route("/main")
@app.route("/")
def welcome_page():
    return render_template("main.html", title="DOODLE - проверь свой код!", **base_config())


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')