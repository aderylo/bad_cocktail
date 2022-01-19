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
        values = session.query(Ingredient).all()
        results = [value.dict() for value in values]
        return (json.dumps(results), 200, {"content_type": "application/json"})


@app.route("/cocktails")
def get_cocktails():
    ingredients = [13, 110, 78, 89, 57]  # ingredient_ids of Mojito
    max_add = 1
    total = len(ingredients) + max_add

    query = """
    WITH CTE1 AS (
    SELECT cocktail_id, COUNT(*) all_ing
    FROM cocktail_ingredients
    GROUP BY cocktail_id
    HAVING COUNT(*) < :total),
     CTE2 AS (
         SELECT cocktail_id, COUNT(*) listed_ingredients
         FROM cocktail_ingredients
         WHERE ingredient_id IN :essential
         GROUP BY cocktail_id)
    SELECT CTE2.*, all_ing
    FROM CTE2
            LEFT JOIN CTE1 ON CTE1.cocktail_id = CTE2.cocktail_id
    WHERE all_ing - listed_ingredients <= :max_additional_ing
    ORDER BY listed_ingredients desc;
    """
    with Session(engine) as session:
        values = session.execute(
            query,
            {
                "total": total,
                "max_additional_ing": max_add,
                "essential": tuple(ingredients),
            },
        )
        results = [dict(value) for value in values]
        return (json.dumps(results), 200, {"content_type": "application/json"})


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
