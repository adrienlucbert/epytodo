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

    def open(self):
        try:
            if self.connected:
                self.close()
            if app.config["DATABASE_SOCK"] == None:
                self.link = sql.connect(host=app.config["DATABASE_HOST"],
                                        user=app.config["DATABASE_USER"],
                                        passwd=app.config["DATABASE_PASS"],
                                        db=app.config["DATABASE_NAME"]
                                        )
            else:
                self.link = sql.connect(unix_socket=app.config["DATABASE_SOCK"],
                                        user=app.config["DATABASE_USER"],
                                        passwd=app.config["DATABASE_PASS"],
                                        db=app.config["DATABASE_NAME"]
                                        )
            self.cursor = self.link.cursor()
            self.connected = True
        except (Exception) as e:
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
    def __init__(self, username=None, id=None):
        self.id = id
        self.name = username
        if self.name != None and self.id != None:
            self.logged = True
        else:
            self.logged = False
        session["logged"] = self.logged
        self.sql = SqlConnect()
        if "logged" in session and session["logged"]:
            self.logged = True
        if "userid" in session:
            self.id = session["userid"]
        if "username" in session:
            self.name = session["username"]

    def register(self, username, passwd):
        if self.logged or username == None or passwd == None:
            return False
        try:
            self.name = username
            self.sql.open()
            self.sql.execute("INSERT INTO user (username, password) VALUES ('%s', '%s')"
                             % (self.name, passwd))
            self.sql.commit()
            self.sql.execute("SELECT user_id FROM user WHERE username='%s' LIMIT 1"
                             % (self.name))
            self.id = self.sql.fetchone()[0]
            self.logged = True
            self.sql.close()
        except (Exception) as e:
            print(e)
            return False
        session["username"] = self.name
        session["id"] = self.id
        session["logged"] = self.logged
        return True

    def login(self, username=None, passwd=None):
        if self.logged or username == None or passwd == None:
            return False
        try:
            self.name = username
            self.sql.open()
            self.sql.execute("SELECT COUNT(1) FROM user WHERE username='%s' AND password='%s'"
                             % (username, passwd))
            self.logged = self.sql.fetchone()[0] > 0
            if self.logged == False:
                self.name = None
                return False
            self.sql.execute("SELECT user_id FROM user WHERE username='%s' LIMIT 1"
                             % (self.name))
            self.id = self.sql.fetchone()[0]
            self.sql.close()
        except (Exception) as e:
            print(e)
            self.name = None
            self.id = None
            return False
        session["username"] = self.name
        session["id"] = self.id
        return self.logged

    def logout(self):
        if self.logged:
            self.logged = False
            session.pop("logged", None)
            session.pop("username", None)
            session.pop("id", None)
            return True
        else:
            return False

    def getTaskById(self, task_id=None):
        if self.logged == False or task_id == None:
            return False
        try:
            self.sql.open()
            self.sql.execute("SELECT COUNT(1) FROM user_has_task WHERE fk_task_id='%d' AND fk_user_id='%d'"
                             % (task_id, self.id))
            if self.sql.fetchone()[0] <= 0:
                return False
            self.sql.execute("SELECT * FROM task WHERE task_id='%d' LIMIT 1"
                             % (task_id))
            task = self.sql.fetchone()
            self.sql.close()
            return task
        except (Exception) as e:
            print(e)
            return False

    def getAllTasks(self):
        if self.logged == False:
            return False
        try:
            self.sql.open()
            self.sql.execute("SELECT * FROM task WHERE user_id='%d'"
                             % (self.id))
            tasks = list(self.sql.fetchall())
            self.sql.close()
            return tasks
        except (Exception) as e:
            print(e)
            return False

class Task:
    def __init__(self, sql=None):
        if sql == None:
            self.sql = SqlConnect()
        else:
            self.sql = sql
        self.id = None
        self.title = None
        self.begin = None
        self.end = None
        self.status = "not started"
    
    def create(self, title=None, begin=None, end=None, status=None):
        if title == None or begin == None or end == None:
            return False
        try:
            self.sql.execute("INSERT INTO task (title, begin, end, status) VALUES ('%s', '%s', '%s', '%s')"
                             % (title, begin, end, status))
            self.sql.cursor.commit()
        except (Exception) as e:
            print(e)
            return False
        return True

    def delete(self):
        if self.id == None:
            return False
        try:
            self.sql.execute("DELETE FROM task WHERE task_id=%d"
                             % (self.id))
            self.sql.cursor.commit()
        except (Exception) as e:
            print(e)
            return False
        return True

    def update(self, title=None, begin=None, end=None, status=None):
        if self.id == None:
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
                                 % (key, val, self.id))
            self.sql.cursor.commit()
        except (Exception) as e:
            print(e)
            return False
        return True