import os
import re

import pandas as pd
from db import clean_up_db, create_db_and_tables, engine
from models import Cocktail, Glassware, Ingredient
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

        session.commit()


if __name__ == "__main__":
    data = dowload_dataset_from_kaggle()
    save_data(data)
