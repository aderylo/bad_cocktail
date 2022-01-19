import itertools
import json

from db import engine
from flask import Flask, request
from models import Cocktail, Ingredient
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
def get_cocktails_by_ingredients():
    max_add = int(request.args.get("count"))
    ingredient_ids = [int(id) for id in request.args.get("ids").split(",")]
    total = len(ingredient_ids) + max_add
    drink_ids = []

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

    with Session(engine) as session:
        for quantity in range(len(ingredient_ids)):
            combinations = itertools.combinations(set(ingredient_ids), quantity + 1)
            for subset in combinations:
                values = session.execute(
                    query,
                    {
                        "total": total,
                        "max_additional_ing": max_add,
                        "essential": tuple(subset),
                    },
                )
                drink_ids = drink_ids + [value["cocktail_id"] for value in values]

    drink_ids = set(drink_ids)
    result = get_cocktails(drink_ids)
    return (json.dumps(result), 200, {"content_type": "application/json"})


@app.route("/drinks")
def get_cocktails_by_ids():
    ids = request.args.get("ids")
    ids = [int(id) for id in ids.split(",")]
    cocktails = get_cocktails(ids)
    return (json.dumps(cocktails), 200, {"content_type": "application/json"})


def get_cocktails(ids):
    cocktails = []
    results = []
    with Session(engine) as session:
        for id in ids:
            cocktail = session.query(Cocktail).get(id)
            if cocktail:
                cocktails.append(cocktail)

        for cocktail in cocktails:
            ingredients = [ing.dict() for ing in cocktail.ingredients]
            cocktail = cocktail.dict()
            cocktail["ingredients"] = ingredients
            results.append(cocktail)

    return results


if __name__ == "__main__":
    app.run(debug=True)
