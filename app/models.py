##
## EPITECH PROJECT, 2019
## WEB_epytodo_2018
## File description:
## models
##

from flask import session
from app import app
import pymysql as sql

class SqlConnect:
    def __init__(self):
        self.connected = False
        self.link = None
        self.cursor = None

    def open(self, restart=False):
        try:
            if restart == True and self.connected == True:
                self.close()
            elif restart == False and self.connected == True:
                return True
            if app.config["DATABASE_SOCK"] == None:
                self.link = sql.connect(host=app.config["DATABASE_HOST"],
                                        user=app.config["DATABASE_USER"],
                                        passwd=app.config["DATABASE_PASS"],
                                        db=app.config["DATABASE_NAME"],
                                        cursorclass=sql.cursors.DictCursor
                                        )
            else:
                self.link = sql.connect(unix_socket=app.config["DATABASE_SOCK"],
                                        user=app.config["DATABASE_USER"],
                                        passwd=app.config["DATABASE_PASS"],
                                        db=app.config["DATABASE_NAME"],
                                        cursorclass=sql.cursors.DictCursor
                                        )
            self.cursor = self.link.cursor()
            self.connected = True
        except (Exception) as e:
            print("SqlConnect.open: ")
            print(e)
            return False
        return True

    def close(self):
        self.cursor.close()
        self.link.close()
        self.connected = False

    def execute(self, cmd=None):
        if cmd == None:
            return False
        return self.cursor.execute(cmd)

    def commit(self):
        return self.link.commit()

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

class User:
    def __init__(self, sql=None, username=None, id=None):
        self.id = id
        self.name = username
        self.logged = username != None
        if sql == None:
            self.sql = SqlConnect()
        else:
            self.sql = sql

    def register(self, username, passwd):
        if self.logged or username == None or passwd == None:
            return 2
        try:
            self.sql.open()
            self.name = username
            self.sql.execute("SELECT COUNT(1) FROM user WHERE username='%s' AND password='%s'"
                             % (username, passwd))
            if self.sql.fetchone()["COUNT(1)"] > 0:
                return 1
            self.sql.execute("INSERT INTO user (username, password) VALUES ('%s', '%s')"
                             % (self.name, passwd))
            self.sql.commit()
            self.sql.execute("SELECT LAST_INSERT_ID()")
            self.id = self.sql.fetchone()["LAST_INSERT_ID()"]
            self.logged = True
        except (Exception) as e:
            print("User.register: ")
            print(e)
            return 2
        session["username"] = self.name
        session["id"] = self.id
        session["logged"] = self.logged
        return 0

    def login(self, username=None, passwd=None):
        if self.logged or username == None or passwd == None:
            return False
        try:
            self.sql.open()
            self.name = username
            self.sql.execute("SELECT COUNT(1) FROM user WHERE username='%s' AND password='%s'"
                             % (username, passwd))
            if self.sql.fetchone()["COUNT(1)"] > 0:
                self.logged = True
            else:
                self.name = None
                return 1
            self.sql.execute("SELECT user_id FROM user WHERE username='%s' LIMIT 1"
                             % (self.name))
            self.id = self.sql.fetchone()["user_id"]
        except (Exception) as e:
            print("User.login: ")
            print(e)
            self.name = None
            self.id = None
            return 2
        session["username"] = self.name
        session["id"] = self.id
        return 0

    def logout(self):
        if self.logged:
            self.logged = False
            session.pop("logged", None)
            session.pop("username", None)
            session.pop("id", None)
            return 0
        else:
            return 1

    def getInfo(self):
        if self.logged:
            try:
                self.sql.open()
                self.sql.execute("SELECT username, password FROM user WHERE user_id='%d' LIMIT 1"
                                 % (self.id))
                res = self.sql.fetchone()
                return 0, res
            except (Exception) as e:
                print("User.getInfo: ")
                print(e)
                return 2, None

    def createTask(self, title=None, begin=None, end=None, status=None):
        if self.logged == False:
            return False
        task = Task(self.sql)
        if task.create(title, begin, end, status) == False and task.id != None:
            return False
        try:
            self.sql.open()
            self.sql.execute("INSERT INTO user_has_task (fk_user_id, fk_task_id) VALUES (%d, %d)"
                             % (self.id, task.id))
            self.sql.commit()
        except (Exception) as e:
            print("User.createTask: ")
            print(e)
            return False
        return True

    def hasTask(self, task_id=None):
        task = self.getTaskById(task_id)
        if task == False:
            return False
        else:
            return True

    def deleteTaskById(self, task_id):
        task = self.getTaskById(task_id)
        if task == False:
            return False
        try:
            self.sql.open()
            self.sql.execute("DELETE FROM user_has_task WHERE fk_task_id=%d"
                             % (task.id))
            self.sql.commit()
        except (Exception) as e:
            print("User.deleteTask: ")
            print(e)
            return False
        return task.delete(task_id)

    def updateTaskById(self, task_id, title=None, begin=None, end=None, status=None):
        task = self.getTaskById(task_id)
        if task == None:
            return False
        return task.update(task_id, title, begin, end, status)

    def getTaskById(self, task_id=None):
        if self.logged == False or task_id == None:
            return False
        try:
            self.sql.open()
            self.sql.execute("SELECT COUNT(1) FROM user_has_task WHERE fk_task_id='%d' AND fk_user_id='%d'"
                             % (task_id, self.id))
            if self.sql.fetchone()["COUNT(1)"] <= 0:
                return False
            self.sql.execute("SELECT * FROM task WHERE task_id='%d' LIMIT 1"
                             % (task_id))
            res = self.sql.fetchone()
            return Task(self.sql, res["id"], res["title"], res["begin"], res["end"], res["status"])
        except (Exception) as e:
            print("User.getTaskById: ")
            print(e)
            return False

    def getAllTasks(self):
        if self.logged == False:
            return False
        try:
            tasks = []
            self.sql.open()
            self.sql.execute("SELECT fk_task_id FROM user_has_task WHERE fk_user_id='%d'"
                             % (self.id))
            tasks_ids = list(self.sql.fetchall())
            for task_id in tasks_ids:
                self.sql.execute("SELECT * FROM task WHERE task_id='%d' LIMIT 1"
                    % (task_id["fk_task_id"]))
                tasks.append(self.sql.fetchone())
            return tasks
        except (Exception) as e:
            print("User.getAllTasks: ")
            print(e)
            return False

class Task:
    def __init__(self, sql=None, id=None, title=None, begin=None, end=None, status=None):
        if sql == None:
            self.sql = SqlConnect()
        else:
            self.sql = sql
        self.id = id
        self.title = title
        self.begin = begin
        self.end = end
        self.status = status
        if self.status == None:
            self.status = "not started"
    
    def create(self, title=None, begin=None, end=None, status=None):
        if title == None or begin == None or end == None:
            return False
        try:
            if status == None:
                status = "not started"
            self.sql.open()
            self.sql.execute("INSERT INTO task (title,begin,end,status) VALUES ('%s', '%s', '%s', '%s')"
                             % (title, begin, end, status))
            self.sql.commit()
            self.sql.execute("SELECT LAST_INSERT_ID()")
            self.id = self.sql.fetchone()[0]
        except (Exception) as e:
            print("Task.create: ")
            print(e)
            return False
        return True

    def delete(self, task_id):
        if task_id == None:
            return False
        try:
            self.sql.execute("DELETE FROM task WHERE task_id=%d"
                             % (task_id))
            self.sql.commit()
        except (Exception) as e:
            print("Task.delete: ")
            print(e)
            return False
        return True

    def update(self, task_id, title=None, begin=None, end=None, status=None):
        if task_id == None:
            return False
        to_update = {}
        try:
            if title != None:
                to_update["title"] = title
            if begin != None:
                to_update["begin"] = begin
            if end != None:
                to_update["end"] = end
            if status != None:
                to_update["status"] = status
            for key, val in to_update:
                self.sql.execute("UPDATE task SET %s='%s' WHERE task_id=%d"
                                 % (key, val, task_id))
            self.sql.commit()
        except (Exception) as e:
            print("Task.update: ")
            print(e)
            return False
        return True