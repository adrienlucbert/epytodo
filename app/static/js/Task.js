class Task {
    constructor(id, title, begin, end, status) {
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
            delete: null,
            update: null
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
        // let actionTd = document.createElement("td");
        // tr.appendChild(actionTd);
        // this.html.action = document.createElement("button");
        // this.html.action.className = "start";
        // this.html.action.innerHTML = "START";
        // this.html.action.onclick = () => {
        //     self.start();
        // };
        // actionTd.appendChild(this.html.action);
        // let restartTd = document.createElement("td");
        // tr.appendChild(restartTd);
        // let restart = document.createElement("button");
        // restartTd.appendChild(restart);
        // restart.className = "restart";
        // restart.innerHTML = "RESTART";
        // restart.onclick = () => {
        //     self.restart();
        // };
    }

    update() {
        let self = this;
        fetch("app/back/serviceStatus.php", {
            method: "POST",
            body: self.formData
        })
        .then(data => data.text())
        .then(text => self.status = text)
        .catch(error => console.log(error));

        if (this.status == this.html.status.className)
            return;
        if (this.status == "online") {
            this.html.log.innerHTML = "No issue";
            this.html.status.className = this.status;
            this.html.status.innerHTML = "Online";
            this.html.action.className = "stop";
            this.html.action.innerHTML = "STOP";
            this.html.action.onclick = () => {
                self.stop();
            };
        } else {
            this.html.log.innerHTML = "Service not running";
            this.html.status.className = this.status;
            this.html.status.innerHTML = "Offline";
            this.html.action.className = "start";
            this.html.action.innerHTML = "START";
            this.html.action.onclick = () => {
                self.start();
            };
        }
    }
}