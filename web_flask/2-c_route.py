#!/usr/bin/python3
"""This script starts a Flask web application.
"""
from flask import Flask
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """ """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """ """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_text(text):
    """ """
    return f"C {' '.join(text.split('_'))}"


if __name__ == "__main__":
    app.run()
