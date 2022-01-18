import os
import re

import pandas as pd
from db import clean_up_db, create_db_and_tables, engine
from models import Cocktail, CocktailIngredient, Glassware, Ingredient
from sqlmodel import Session


def dowload_dataset_from_kaggle() -> pd.DataFrame:
    os.system("kaggle datasets download -d ai-first/cocktail-ingredients")
    os.system("unzip cocktail-ingredients.zip")
    os.system("rm cocktail-ingredients.zip")
    df = pd.read_csv("all_drinks.csv")
    os.system("rm all_drinks.csv")
    return df


def save_data(data: pd.DataFrame):
    clean_up_db()
    create_db_and_tables()
    with Session(engine) as session:

        for drink_dict in data.T.to_dict().values():

            glass = (
                session.query(Glassware)
                .filter(Glassware.name == drink_dict["strGlass"])
                .first()
            )
            if not glass:
                glass = Glassware(name=drink_dict["strGlass"])
                session.add(glass)

            for col in data.columns:
                if re.match("strIngredient.*", col) and str(drink_dict[col]) != "nan":
                    ingredient = (
                        session.query(Ingredient)
                        .filter(Ingredient.name == drink_dict[col])
                        .first()
                    )
                    if not ingredient:
                        ingredient = Ingredient(name=drink_dict[col])
                        session.add(ingredient)

        session.commit()
        glasses = pd.read_sql_table("glassware", engine)
        ingredients = pd.read_sql_table("ingredients", engine)

        for drink_dict in data.T.to_dict().values():
            drink = (
                session.query(Cocktail)
                .filter(Cocktail.id == drink_dict["idDrink"])
                .first()
            )

            if not drink:
                drink = Cocktail(
                    id=drink_dict["idDrink"],
                    name=drink_dict["strDrink"],
                    instructions=drink_dict["strInstructions"],
                    category=drink_dict["strCategory"],
                    phot=drink_dict["strDrinkThumb"],
                    glassId=glasses[glasses["name"] == drink_dict["strGlass"]][
                        "id"
                    ].values.tolist()[0],
                )
                session.add(drink)

            cocktail_ingredient_dict = {}
            for col in data.columns:

                if re.match("strIngredient.*", col) and str(drink_dict[col]) != "nan":
                    index = re.findall("[0-9]+$", col)[-1]
                    element_id = ingredients.loc[
                        ingredients["name"] == drink_dict[col]
                    ]["id"].values.tolist()[0]
                    id_pair = (drink_dict["idDrink"], element_id)
                    measure = cocktail_ingredient_dict.get(id_pair)

                    if measure is None:
                        cocktail_ingredient_dict[id_pair] = drink_dict[
                            "strMeasure" + str(index)
                        ]

                    else:
                        cocktail_ingredient_dict[id_pair] = (
                            measure + "& " + drink_dict["strMeasure" + str(index)]
                        )

            for key in cocktail_ingredient_dict.keys():
                if cocktail_ingredient_dict[key] == "\n":
                    cocktail_ingredient_dict[key] = None
                session.add(
                    CocktailIngredient(
                        cocktail_id=key[0],
                        ingredient_id=key[1],
                        measure=cocktail_ingredient_dict[key],
                    )
                )

        session.commit()


if __name__ == "__main__":
    data = dowload_dataset_from_kaggle()
    save_data(data)
