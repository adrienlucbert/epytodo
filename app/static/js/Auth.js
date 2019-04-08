class Auth {
    constructor() {
        let self = this;
        this.view = null;
        this.form = document.querySelector("section#authenticator form");
        this.username = null;
        this.logged = false;
        fetch("/static/json/forms.json")
        .then(data => data.json())
        .then(json => self.templates = json)
        .catch(error => console.error(error))
    }

    setLogged(status) {
        if (status) {
            this.logged = true;
            this.view.viewLoggedIn();
        } else {
            this.logged = false;
            this.view.viewLoggedOut();
        }
    }

    createForm(templateName) {
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
            let field = document.createElement("input");
            form.appendChild(field);
            field.name = fieldName;
            field.type = template[fieldName].type;
            field.autocomplete = "off";
            field.placeholder = template[fieldName].placeholder;
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

    prompt(templateName) {
        let self = this;
        this.createForm(templateName);
        document.body.classList.add("blur");
        document.querySelector("#authenticator").classList.add("active");
        this.form.reset();
        this.form[0].focus();
        this.form.onsubmit = (e) => {
            e.preventDefault();
            self.form.querySelectorAll("input").forEach(field => {
                field.setAttribute("disabled", "disabled");
            });
            if (templateName == "Signin")
                self.login(self.form.username.value, self.form.password.value);
            else if (templateName == "Signup")
                self.register(self.form.username.value, self.form.password.value, self.form.confirm.value);
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

    register(uname, passwd, confirmpsw) {
        let self = this;
        if (passwd != confirmpsw) {
            console.error("Passwords do not match.");
            self.form.querySelectorAll("input").forEach(field => {
                field.classList.add("invalid-input");
            });
            self.form.onclick = () => {
                self.form.querySelectorAll("input").forEach(field => {
                    field.classList.remove("invalid-input");
                });
            }
            setTimeout(() => {
                self.form.querySelectorAll("input").forEach(field => {
                    field.classList.remove("invalid-input");
                });
            }, 10000);
            return;
        }
        let formData = {
            "username":uname,
            "password":passwd
        };
        fetch("/register", {
            headers: {
                'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify(formData)
        })
        .then(data => data.json())
        .then(json => {
            self.form.querySelectorAll("input").forEach(field => {
                field.removeAttribute("disabled");
            });
            if (json.result) {
                self.setLogged(true);
                self.unprompt();
            } else {
                console.error(json.error);
                self.form.querySelectorAll("input").forEach(field => {
                    field.classList.add("invalid-input");
                });
                self.form.onclick = () => {
                    self.form.querySelectorAll("input").forEach(field => {
                        field.classList.remove("invalid-input");
                    });
                }
                setTimeout(() => {
                    self.form.querySelectorAll("input").forEach(field => {
                        field.classList.remove("invalid-input");
                    });
                }, 10000);
            }
        })
        .catch(error => console.error(error));
    }

    login(uname, passwd) {
        let self = this;
        let formData = {
            "username":uname,
            "password":passwd
        };
        fetch("/signin", {
            headers: {
                'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify(formData)
        })
        .then(data => data.json())
        .then(json => {
            self.form.querySelectorAll("input").forEach(field => {
                field.removeAttribute("disabled");
            });
            if (json.result) {
                self.setLogged(true);
                self.unprompt();
            } else {
                console.error(json.error);
                self.form.querySelectorAll("input").forEach(field => {
                    field.classList.add("invalid-input");
                });
                self.form.onclick = () => {
                    self.form.querySelectorAll("input").forEach(field => {
                        field.classList.remove("invalid-input");
                    });
                }
                setTimeout(() => {
                    self.form.querySelectorAll("input").forEach(field => {
                        field.classList.remove("invalid-input");
                    });
                }, 10000);
            }
        })
        .catch(error => console.error(error));
    }

    logout() {
        let self = this;
        this.logged = false;
        fetch("/signout", {
            method: "POST"
        })
        .then(data => data.json())
        .then((json) => {
            if (json.result) {
                self.setLogged(false);
                document.onkeypress = null;
            } else {
                console.error(json.error);
            }
        })
        .catch(error => console.error(error));
    }
}