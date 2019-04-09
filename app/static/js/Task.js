class Task {
    constructor(view, id=null, title=null, begin=null, end=null, status=null) {
        this.view = view;
        this.id = id;
        this.title = title;
        this.begin = begin;
        this.end = end;
        this.status = status;
        this.html = {
            title: null,
            begin: null,
            end: null,
            status: null,
            update: null,
            delete: null
        };
    }

    addToTable() {
        let self = this;
        let table = document.querySelector("section#list table");
        let tr = document.createElement("tr");
        table.appendChild(tr);
        tr.id = this.id;
        this.html.title = document.createElement("td");
        tr.appendChild(this.html.title);
        this.html.title.innerHTML = this.title;
        this.html.status = document.createElement("td");
        this.html.status.innerHTML = this.status;
        tr.appendChild(this.html.status);
        this.html.begin = document.createElement("td");
        this.html.begin.innerHTML = this.begin;
        tr.appendChild(this.html.begin);
        this.html.end = document.createElement("td");
        this.html.end.innerHTML = this.end;
        tr.appendChild(this.html.end);
        let updateTd = document.createElement("td");
        tr.appendChild(updateTd);
        this.html.update = document.createElement("button");
        this.html.update.className = "update";
        this.html.update.innerHTML = "Update";
        this.html.update.onclick = () => {
            let data = {
                id:self.id,
                title:self.title,
                begin:new Date(self.begin).toISOString().slice(0,16),
                end:new Date(self.end).toISOString().slice(0,16),
                status:self.status
            };
            self.view.prompt("Update task", data);
        };
        updateTd.appendChild(this.html.update);
        let deleteTd = document.createElement("td");
        tr.appendChild(deleteTd);
        this.html.delete = document.createElement("button");
        this.html.delete.className = "delete";
        this.html.delete.innerHTML = "Delete";
        this.html.delete.onclick = () => {
            self.delete();
        };
        deleteTd.appendChild(this.html.delete);
    }

    delete() {
        let self = this;
        fetch("/user/task/del/" + self.id, {
            method: "POST"
        })
        .then(data => data.json())
        .then(json => {
            if (json.result) {
                view.loadTasks();
            } else {
                console.error(json.error);
            }
        })
        .catch(error => console.error(error));
    }

    create(title=null, begin=null, end=null, status=null) {
        let self = this;
        let formData = {
            "title":title,
            "begin":begin,
            "end":end,
            "status":status
        };
        fetch("/user/task/add", {
            headers: {
                'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify(formData)
        })
        .then(data => data.json())
        .then(json => {
            self.view.form.querySelectorAll("input, select").forEach(field => {
                field.removeAttribute("disabled");
            });
            if (json.result) {
                self.view.unprompt();
                self.view.loadTasks();
            } else {
                console.error(json.error);
                self.view.form.querySelectorAll("input, select").forEach(field => {
                    field.classList.add("invalid-input");
                });
                self.view.form.onclick = () => {
                    self.view.form.querySelectorAll("input, select").forEach(field => {
                        field.classList.remove("invalid-input");
                    });
                }
                setTimeout(() => {
                    self.view.form.querySelectorAll("input, select").forEach(field => {
                        field.classList.remove("invalid-input");
                    });
                }, 10000);
            }
        })
        .catch(error => console.error(error));
    }

    update(id=null, title=null, begin=null, end=null, status=null) {
        let self = this;
        if (id == null) {
            console.error("Invalid task id");
            return;
        }
        let formData = {
            "title":title,
            "begin":begin,
            "end":end,
            "status":status
        };
        fetch("/user/task/" + id, {
            headers: {
                'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify(formData)
        })
        .then(data => data.json())
        .then(json => {
            self.view.form.querySelectorAll("input, select").forEach(field => {
                field.removeAttribute("disabled");
            });
            if (json.result) {
                self.view.unprompt();
                self.view.loadTasks();
            } else {
                console.error(json.error);
                self.view.form.querySelectorAll("input, select").forEach(field => {
                    field.classList.add("invalid-input");
                });
                self.view.form.onclick = () => {
                    self.view.form.querySelectorAll("input, select").forEach(field => {
                        field.classList.remove("invalid-input");
                    });
                }
                setTimeout(() => {
                    self.view.form.querySelectorAll("input, select").forEach(field => {
                        field.classList.remove("invalid-input");
                    });
                }, 10000);
            }
        })
        .catch(error => console.error(error));
    }
}