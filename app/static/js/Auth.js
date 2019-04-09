class Auth {
    constructor() {
        let self = this;
        this.view = null;
        this.username = null;
        this.logged = false;
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
                self.view.unprompt();
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
            self.view.form.querySelectorAll("input").forEach(field => {
                field.removeAttribute("disabled");
            });
            if (json.result) {
                self.setLogged(true);
                self.view.unprompt();
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