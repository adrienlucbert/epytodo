##
## EPITECH PROJECT, 2019
## WEB_epytodo_2018
## File description:
## views
##

from flask import Flask, session, render_template, json
from app.models import User
from app import app

@app.route('/', methods=['GET'])
def route_home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def route_register():
    return render_template('index.html')

@app.route('/signin', methods=['POST'])
def route_signin():
    return render_template('index.html')

@app.route('/signout', methods=['POST'])
def route_signout():
    return render_template('index.html')

@app.route('/user', methods=['GET'])
def route_view_user():
    return render_template('index.html')

@app.route('/user/task', methods=['GET'])
def route_view_all_tasks():
    return render_template('index.html')

@app.route('/user/task/<id>', methods=['GET'])
def route_view_task():
    return render_template('index.html')

@app.route('/user/task/<id>', methods=['POST'])
def route_update_task():
    return render_template('index.html')

@app.route('/user/task/add', methods=['POST'])
def route_task_add():
    return render_template('index.html')

@app.route('/user/task/del/<id>', methods=['POST'])
def route_task_del():
    return render_template('index.html')