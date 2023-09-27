#!/usr/bin/python3
"""This script starts a Flask web application.
"""
from models import storage
from os import getenv
from flask import Flask, render_template
app = Flask(__name__)


@app.teardown_appcontext
def remove(exception=None):
    """ """
    storage.close()


@app.route("/cities_by_states", strict_slashes=False)
def list_state():
    state_list = storage.all("State").values()
    sorted_state_list = sorted(state_list, key=lambda state: state.name)
    state_city_list = []
    for state in sorted_state_list:
        city_list = state.cities
        if city_list:
            state_city_list.append(city_list)
        else:
            state_city_list.append([])

    return render_template("8-cities_by_states.html", states=sorted_state_list,
                           cities=state_city_list, length=len(state_list))


if __name__ == "__main__":
    app.run()
