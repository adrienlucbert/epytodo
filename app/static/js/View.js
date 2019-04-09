class View {
    constructor() {
        let self = this;
        this.auth = new Auth();
        this.auth.view = this;
        if (this.auth.logged) {
            this.viewLoggedIn();
        } else {
            this.viewLoggedOut();
        }
        this.tasks = [];
        this.templates = null;
        this.form = document.querySelector("section#authenticator form");
        this.loadTemplates();
        document.querySelector("button.add").onclick = () => {
            self.prompt("Add task");
        };
    }

    loadTemplates() {
        let self = this;
        fetch("/static/json/forms.json")
        .then(data => data.json())
        .then(json => self.templates = json)
        .catch(error => console.error(error))
    }

    resetTable() {
        let table = document.querySelector("section#list table");
        table.querySelectorAll("tr:not(.tr-static)").forEach(tr => {
            tr.remove();
        });
    }

    viewLoggedIn() {
        let self = this;
        document.querySelector("#general").classList.remove("active");
        document.querySelector("#list").classList.add("active");
        document.querySelector("header button:first-of-type").innerHTML = "Signout";
        document.querySelector("header button:first-of-type").onclick = () => {
            self.auth.logout();
        };
        document.querySelector("header button:last-of-type").classList.remove("active");
        this.loadTasks();
    }
    
    viewLoggedOut() {
        let self = this;
        document.querySelector("#list").classList.remove("active");
        document.querySelector("#general").classList.add("active");
        document.querySelector("header button:last-of-type").innerHTML = "Signup";
        document.querySelector("header button:last-of-type").onclick = () => {
            self.prompt("Signup");
        };
        document.querySelector("header button:last-of-type").classList.add("active");
        document.querySelector("header button:first-of-type").innerHTML = "Signin";
        document.querySelector("header button:first-of-type").onclick = () => {
            self.prompt("Signin");
        };
    }

    createForm(templateName, data=null) {
        if (!this.templates) {
            console.error("No form template available at the moment.");
            return;
        }
        let template = this.templates[templateName];
        let section = document.querySelector("section#authenticator");
        if (section)
            section.remove()
        section = document.createElement("section");
        section.id = "authenticator";
        section.className = "noblur";
        document.body.appendChild(section);
        let form = document.createElement("form");
        section.appendChild(form);
        let legend = document.createElement("legend");
        form.appendChild(legend);
        legend.innerHTML = "Authentication";
        let p = document.createElement("p");
        form.appendChild(p);
        p.innerHTML = "Please enter your creditentials herebelow.";
        for (let fieldName in template) {
            let field = template[fieldName];
            let input = null;
            switch (field.type) {
                case "select":
                    input = document.createElement("select");
                    form.appendChild(input);
                    field.options.forEach(option => {
                        let optionField = document.createElement("option");
                        input.appendChild(optionField);
                        input.name = fieldName;
                        optionField.value = option;
                        optionField.innerHTML = option;
                    });
                break;
                case "datetime-local":
                    input = document.createElement("input");
                    form.appendChild(input);
                    input.name = fieldName;
                    input.type = field.type;
                break;
                default:
                    input = document.createElement("input");
                    form.appendChild(input);
                    input.name = fieldName;
                    input.type = field.type;
                    input.autocomplete = "off";
                    input.placeholder = field.placeholder;
                break;
            }
            if (data != null && field.datavalue && data[field.datavalue]) {
                input.value = data[field.datavalue];
            }
        }
        let submit = document.createElement("input");
        form.appendChild(submit);
        submit.type = "submit";
        submit.value = templateName;
        this.form = form;
    }

    unprompt() {
        this.form.querySelectorAll("input").forEach(field => {
            field.blur();
        });
        document.body.classList.remove("blur");
        document.querySelector("#authenticator").classList.remove("active");
    }

    prompt(templateName, data=null) {
        let self = this;
        if (this.form != null)
            this.form.reset();
        this.createForm(templateName, data);
        document.body.classList.add("blur");
        document.querySelector("#authenticator").classList.add("active");
        this.form[0].focus();
        this.form.onsubmit = (e) => {
            e.preventDefault();
            self.form.querySelectorAll("input").forEach(field => {
                field.setAttribute("disabled", "disabled");
            });
            switch(templateName) {
                case "Signin":
                    self.auth.login(self.form.username.value, self.form.password.value);
                break;
                case "Signup":
                    self.auth.register(self.form.username.value, self.form.password.value, self.form.confirm.value);
                break;
                case "Add task":
                    let add_title = self.form.title.value;
                    let add_begin = self.form.begin.value;
                    let add_end = self.form.end.value;
                    let add_status = self.form.status.value;
                    self.createTask(add_title, add_begin, add_end, add_status);
                break;
                case "Update task":
                    let upd_id = self.form.id.value;
                    let upd_title = self.form.title.value;
                    let upd_begin = self.form.begin.value;
                    let upd_end = self.form.end.value;
                    let upd_status = self.form.status.value;
                    self.updateTask(upd_id, upd_title, upd_begin, upd_end, upd_status);
                break;
                default:
                    console.error("Form template '"+templateName+"' is not handled.");
                    self.unprompt();
                break;
            }
            if (templateName == "Signin")
                self.auth.login(self.form.username.value, self.form.password.value);
            else if (templateName == "Signup")
                self.auth.register(self.form.username.value, self.form.password.value, self.form.confirm.value);
        };
        document.onkeydown = (e) => {
            if (e.keyCode == 27) {
                self.unprompt();
            }
        };
        document.onmousedown = (e) => {
            if (e.target == document.querySelector("#authenticator")) {
                self.unprompt();
            }
        };
    }

    displayTasks() {
        this.resetTable();
        this.tasks.forEach(task => {
            task.addToTable();
        });
    }

    createTask(title=null, begin=null, end=null, status=null) {
        let task = new Task(this);

        task.create(title, begin, end, status);
    }

    updateTask(id=null, title=null, begin=null, end=null, status=null) {
        let task = new Task(this);

        task.update(id, title, begin, end, status);
    }

    loadTasks() {
        this.tasks = [];
        let self = this;
        if (this.auth.logged == false) {
            console.error("You must be logged in");
            return;
        }
        fetch("/user/task")
        .then(data => data.json())
        .then(json => {
            if (json.result) {
                let tasks = json.result.tasks;
                Object.keys(tasks).forEach(task => {
                    let id = parseInt(task);
                    let title = tasks[task]["title"];
                    let begin = tasks[task]["begin"];
                    let end = tasks[task]["end"];
                    let status = tasks[task]["status"];
                    self.tasks.push(new Task(self, id, title, begin, end, status));
                });
                self.displayTasks();
            } else {
                console.error(json.error);
            }
        })
        .catch(error => console.error(error));
    }
}