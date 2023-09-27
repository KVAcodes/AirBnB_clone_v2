#!/usr/bin/python3
"""This script starts a Flask web application.
"""
from models import storage
from flask import Flask, render_template
app = Flask(__name__)


@app.teardown_appcontext
def remove(exception=None):
    """ """
    storage.close()


@app.route("/states_list", strict_slashes=False)
def list_state():
    state_list = storage.all("State").values()
    nameId_list = [(state.id, state.name) for state in
                   state_list]
    nameId_list = sorted(nameId_list, key=lambda x: x[1])
    return render_template("7-states_list.html", nameId_list=nameId_list)


if __name__ == "__main__":
    app.run()
