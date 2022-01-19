import itertools
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
    ids = request.args.get("ids")
    count = request.args.get("count")
    ids = [int(i) for i in ids.split(",")]
    ingredients = ids
    max_add = int(count)
    total = len(ingredients) + max_add
    result = []
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
    SELECT CTE2.cocktail_id
    FROM CTE2
            LEFT JOIN CTE1 ON CTE1.cocktail_id = CTE2.cocktail_id
    WHERE all_ing - listed_ingredients <= :max_additional_ing
    ORDER BY listed_ingredients desc;
    """

    for quantity in range(len(ingredients)):
        combinations = itertools.combinations(set(ingredients), quantity + 1)
        for subset in combinations:
            with Session(engine) as session:
                values = session.execute(
                    query,
                    {
                        "total": total,
                        "max_additional_ing": max_add,
                        "essential": tuple(subset),
                    },
                )
                result = result + [value["cocktail_id"] for value in values]

    result = set(result)
    result = [{"cocktail_id": id} for id in result]

    return (json.dumps(result), 200, {"content_type": "application/json"})


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
