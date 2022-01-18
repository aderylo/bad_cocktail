#!/home/students/mismap/a/ad432952/public_html/api/bin/python3

import json

from db import Session
from flask import Flask, request
from models import Ingredient

app = Flask(__name__)


@app.teardown_appcontext
def cleanup(resp_or_exc):
    Session.remove()


@app.route("/")
def index():
    return "testing"


@app.route("/i")
def get_ingredients():
    values = Session.query(Ingredient).all()
    results = [value.dict() for value in values]
    return (json.dumps(results), 200, {"content_type": "application/json"})


@app.route("/d")
def drinks():
    ids = request.args.get("ids")
    values = [
        {
            "name": "Mohito",
            "id": 2,
            "image_link": "./images/test.jpg",
            "ingridients": ["Vodka", "Sprite", "Lemon"],
        },
        {
            "name": str(ids),
            "id": 3,
            "image_link": "./images/test.jpg",
            "ingridients": ["LOL", "HEHe"],
        },
    ]
    return json.dumps(values)


if __name__ == "__main__":
    app.run(debug=True)
