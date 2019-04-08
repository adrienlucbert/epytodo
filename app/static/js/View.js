class View {
    constructor() {
        this.auth = new Auth();
        this.auth.view = this;
        if (this.auth.logged) {
            this.viewLoggedIn();
        } else {
            this.viewLoggedOut();
        }
        this.tasks = [];
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
        this.resetTable();
        this.loadTasks();
    }
    
    viewLoggedOut() {
        let self = this;
        document.querySelector("#list").classList.remove("active");
        document.querySelector("#general").classList.add("active");
        document.querySelector("header button:last-of-type").innerHTML = "Signup";
        document.querySelector("header button:last-of-type").onclick = () => {
            self.auth.prompt("Signup");
        };
        document.querySelector("header button:last-of-type").classList.add("active");
        document.querySelector("header button:first-of-type").innerHTML = "Signin";
        document.querySelector("header button:first-of-type").onclick = () => {
            self.auth.prompt("Signin");
        };
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
                    self.tasks.push(new Task(id, title, begin, end, status));
                });
                self.tasks.forEach(taskObject => {
                    taskObject.addToTable();
                });
            } else {
                console.error(json.error);
            }
        })
        .catch(error => console.error(error));
    }
}