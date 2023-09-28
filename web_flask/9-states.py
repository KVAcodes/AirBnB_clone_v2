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


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    """display the states in alphabetical order"""
    states = storage.all("State").values()
    state_exists = any(state.id == id for state in states)
    return render_template('9-states.html', states=states,
                           state_id=id,
                           state_exists=state_exists)


if __name__ == "__main__":
    app.run()
