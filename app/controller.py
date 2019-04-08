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

class TaskController(Controller):
    def __init__(self):
        super().__init__()

    def create(self, title=None, begin=None, end=None, status=None):
        return None

    def delete(self, id=None):
        return None

    def update(self, title=None, begin=None, end=None, status=None):
        return None