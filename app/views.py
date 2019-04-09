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
    username = request.json["username"]
    password = request.json["password"]
    controller = UserController()
    return controller.register(username, password)

@app.route('/signin', methods=['POST'])
def route_signin():
    username = request.json["username"]
    password = request.json["password"]
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
    title = request.json["title"]
    begin = request.json["begin"]
    end = request.json["end"]
    status = request.json["status"]
    controller = TaskController()
    return controller.update(task_id, title, begin, end, status)

@app.route('/user/task/add', methods=['POST'])
def route_task_add():
    title = request.json["title"]
    begin = request.json["begin"]
    end = request.json["end"]
    status = request.json["status"]
    controller = TaskController()
    return controller.create(title, begin, end, status)

@app.route('/user/task/del/<int:task_id>', methods=['POST'])
def route_task_del(task_id):
    controller = TaskController()
    return controller.delete(task_id)