from app import app
from flask import Flask, url_for, render_template

@app.route('/index', methods=['GET'])
@app.route('/', methods=['GET'])
def route_home():
    return render_template('index.html')

@app.route('/user/<username>', methods=['POST'])
def route_add_user(username):
    return "User added!\n"