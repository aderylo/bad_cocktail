import os

import pandas as pd
from db import create_db_and_tables, engine
from models import Glassware
from sqlmodel import Session


def dowload_dataset_from_kaggle() -> pd.DataFrame:
    os.system("kaggle datasets download -d ai-first/cocktail-ingredients")
    os.system("unzip cocktail-ingredients.zip")
    os.system("rm cocktail-ingredients.zip")
    df = pd.read_csv("all_drinks.csv")
    os.system("rm all_drinks.csv")
    return df


def save_data(data):
    create_db_and_tables()
    with Session(engine) as session:
        print(session.query(Glassware).get(1))
