##
## EPITECH PROJECT, 2019
## Untitled (Workspace)
## File description:
## controller
##

from flask import Flask, session, render_template, json
from app.models import User, Task, SqlConnect

class Controller:
    def __init__(self):
        self.sql = SqlConnect()
        self.user = User(self.sql, session.get("username"), session.get("id"))
        self.task = Task(self.sql)

    def notLoggedIn(self):
        res = {}
        res["error"] = "you must be logged in"
        return json.dumps(res)

    def taskIdInvalid(self):
        res = {}
        res["error"] = "task id does not exist"
        return json.dumps(res)

    def internalError(self):
        res = {}
        res["error"] = "internal error"
        return json.dumps(res)

class UserController(Controller):
    def __init__(self):
        super().__init__()

    def register(self, username=None, passwd=None):
        if self.user.logged == True:
            return None
        res = {}
        status = self.user.register(username, passwd)
        if status == 0:
            res["result"] = "account created"
        elif status == 1:
            res["error"] = "account already exists"
        else:
            return self.internalError()
        return json.dumps(res)

    def login(self, username=None, passwd=None):
        if self.user.logged == True:
            status = 0
        else:
            status = self.user.login(username, passwd)
        res = {}
        if status == 0:
            res["result"] = "signin successful"
        elif status == 1:
            res["error"] = "login or password does not match"
        else:
            return self.internalError()
        return json.dumps(res)

    def logout(self):
        res = {}
        status = self.user.logout()
        if status == 0:
            res["result"] = "signout successful"
            return json.dumps(res)

    def info(self):
        if self.user.logged == False:
            return self.notLoggedIn()
        status, userInfo = self.user.getInfo()
        res = {}
        if status == 0:
            res["result"] = userInfo
            return json.dumps(res)
        else:
            return self.internalError()

    def getAllTasks(self):
        if self.user.logged == False:
            return self.notLoggedIn()
        res = {}
        status, tasks = self.user.getAllTasks()
        if status == 0:
            res["result"] = {}
            res["result"]["tasks"] = tasks
            return json.dumps(res)
        else:
            return self.internalError()

class TaskController(Controller):
    def __init__(self):
        super().__init__()

    def create(self, title=None, begin=None, end=None, status=None):
        if self.user.logged == False:
            return self.notLoggedIn()
        else:
            ret = self.task.create(title, begin, end, status)
        if ret == False:
            return self.internalError()
        res = {}
        res['result'] = "new task added"
        return json.dumps(res)

    def delete(self, task_id=None):
        if self.user.logged == False:
            return self.notLoggedIn()
        elif self.user.hasTask(task_id) == False:
            return self.taskIdInvalid()
        else:
            status = self.task.delete(task_id)
        if status == False:
            return self.taskIdInvalid()
        res = {}
        res['result'] = "task deleted"
        return json.dumps(res)

    def update(self, task_id=None, title=None, begin=None, end=None, status=None):
        if self.user.logged == False:
            return self.notLoggedIn()
        elif self.user.hasTask(task_id) == False:
            return self.taskIdInvalid()
        else:
            status = self.task.update(title, begin, end, status)
        if status == False:
            return self.internalError()
        res = {}
        res['result'] = "update done"
        return json.dumps(res)

    def info(self, task_id):
        res = {}
        if self.user.logged == False:
            return self.notLoggedIn()
        elif self.user.hasTask(task_id) == False:
            return self.taskIdInvalid()
        else:
            status, task = self.user.getTaskById(task_id)
        if status == 0:
            res["result"] = task.info()
            return json.dumps(res)
        else:
            return self.internalError()