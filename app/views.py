##
## EPITECH PROJECT, 2019
## WEB_epytodo_2018
## File description:
## views
##

from flask import Flask, request, session, render_template, json
from app.controller import UserController, TaskController
from app import app

@app.route('/', methods=['GET'])
def route_home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def route_register():
    username = request.form.get("username")
    password = request.form.get("password")
    controller = UserController()
    return controller.register(username, password)

@app.route('/signin', methods=['POST'])
def route_signin():
    username = request.form.get("username")
    password = request.form.get("password")
    controller = UserController()
    return controller.login(username, password)

@app.route('/signout', methods=['POST'])
def route_signout():
    controller = UserController()
    return controller.logout()

@app.route('/user', methods=['GET'])
def route_view_user():
    controller = UserController()
    return controller.info()

@app.route('/user/task', methods=['GET'])
def route_view_all_tasks():
    controller = UserController()
    return controller.getAllTasks()

@app.route('/user/task/<int:task_id>', methods=['GET'])
def route_view_task(task_id):
    controller = TaskController()
    return controller.info(task_id)

@app.route('/user/task/<int:task_id>', methods=['POST'])
def route_update_task(task_id):
    title = request.form.get("title")
    begin = request.form.get("begin")
    end = request.form.get("end")
    status = request.form.get("status")
    controller = TaskController()
    return controller.task.update(task_id, title, begin, end, status)

@app.route('/user/task/add', methods=['POST'])
def route_task_add():
    title = request.form.get("title")
    begin = request.form.get("begin")
    end = request.form.get("end")
    status = request.form.get("status")
    controller = TaskController()
    return controller.task.create(title, begin, end, status)

@app.route('/user/task/del/<int:task_id>', methods=['POST'])
def route_task_del(task_id):
    controller = TaskController()
    return controller.task.delete(task_id)