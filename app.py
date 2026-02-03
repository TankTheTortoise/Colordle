import json
import random

import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
# from models import Colors
from ColorMath import *
from flask import send_from_directory

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
# db = SQLAlchemy()

global true_color
true_color = random.choice(list(pd.read_csv("static/colors.csv")["Nombre"])).replace(u'\u200b', '').lower()
print(true_color)

@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')

@app.route("/colors")
def colors():
    return send_from_directory("", "static/colors.csv")

# Socketio
@socketio.on('guess')
def my_event(data):
    guess = percent_difference(color_to_hex(true_color), color_to_hex(data["guess"]))
    previous_guesses = data["previous_guesses"]
    guesses = {}
    for g in previous_guesses:
        if color_to_hex(g) != -1:
            guesses.update({g: (percent_difference(color_to_hex(true_color), color_to_hex(g)), color_to_hex(g))})

    socketio.emit("accuracy", {"guess": guess, "previous_guesses": guesses})

@socketio.on('reload_values')
def reload_values(data):
    print(json.loads(data))
    guesses = {}
    for g in json.loads(data)["guesses"]:
        if color_to_hex(g) != -1:
            guesses.update({g: (percent_difference(color_to_hex(true_color), color_to_hex(g)), color_to_hex(g))})

    socketio.emit("reloaded_values", {"reload_guesses": guesses})

@app.route("/truecolor")
def get_color():
    return true_color




if __name__ == '__main__':
    # db.init_app(app)
    socketio.run(app, host='0.0.0.0')
