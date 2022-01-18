import json

from db import engine
from flask import Flask, request
from models import Ingredient
from sqlmodel import Session

app = Flask(__name__)


@app.route("/")
def index():
    return "testing"


@app.route("/ingredients")
def get_ingredients():
    with Session(engine) as session:
        return session.query(Ingredient).all()


@app.route("/drinks")
def drinks():
    ids = request.args.get("ids")
    return json.dumps(
        [
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
    )


if __name__ == "__main__":
    app.run(debug=True)
