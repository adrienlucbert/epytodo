##
## EPITECH PROJECT, 2019
## WEB_epytodo_2018
## File description:
## __init__
##

from flask import Flask

app = Flask(__name__)
app.secret_key = 'epytodo'
app.config.from_object('config')

from app import views