import pymysql as sql

class SqlConnect:
    def __init__(self):
        self.connected = False
        self.link = None
        self.cursor = None

    def open(self):
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

    def close(self):
        self.cursor.close()
        self.link.close()
        self.connected = False

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
            self.sql.execute("INSERT INTO task (id, title, begin, end, status) VALUES (%d, '%s', '%s', '%s', '%s')"
                            % (self.id, title, begin, end, status))
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
                self.sql.execute("UPDATE task SET %s=%s WHERE task_id=%d"
                                % (key, val, self.id))
            self.sql.cursor.commit()
        except (Exception) as e:
            print(e)
            return False
        return True