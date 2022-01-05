import os

import pandas as pd


def dowload_dataset_from_kaggle() -> pd.DataFrame:
    os.system("kaggle datasets download -d ai-first/cocktail-ingredients")
    os.system("unzip cocktail-ingredients.zip")
    os.system("rm cocktail-ingredients.zip")
    df = pd.read_csv("all_drinks.csv")
    os.system("rm all_drinks.csv")
    return df
