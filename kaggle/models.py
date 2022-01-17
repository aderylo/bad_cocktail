from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class CocktailIngredient(SQLModel, table=True):
    __tablename__ = "cocktail_ingredients"
    # __table_args__ = (UniqueConstraint("cocktail_id", "ingredient_id"),)
    cocktail_id: int = Field(foreign_key="cocktails.id", primary_key=True)
    ingredient_id: int = Field(foreign_key="ingredients.id", primary_key=True)
    measure: Optional[str]
    cocktail: "Cocktail" = Relationship(back_populates="ingredient")
    ingrident: "Ingredient" = Relationship(back_populates="cocktails")


class Ingredient(SQLModel, table=True):
    __tablename__ = "ingredients"
    id: int = Field(primary_key=True)
    name: str
    price: Optional[int]
    cocktails: List[CocktailIngredient] = Relationship(
        back_populates="ingrident")


class Cocktail(SQLModel, table=True):
    __tablename__ = "cocktails"
    id: int = Field(primary_key=True)
    name: str
    instructions: str
    category: str
    photo: Optional[str]
    glassId: int = Field(foreign_key="glassware.id")
    glass: "Glassware" = Relationship(back_populates="cocktails")
    ingredients: List[CocktailIngredient] = Relationship(
        back_populates="cocktail")


class Glassware(SQLModel, table=True):
    __tablename__ = "glassware"
    id: int = Field(primary_key=True)
    name: str
    photo: Optional[str]
    cocktails: List[Cocktail] = Relationship(back_populates="glass")


class Garnish(SQLModel, table=True):
    __tablename__ = "garnishes"
    id: int = Field(primary_key=True)
    name: str
    price: Optional[int]


# class CocktailGarnish(SQLModel, table=True):
#     __tablename__ = "cocktail_garnishes"
#     __table_args__ = (UniqueConstraint("cocktail_id", "garnish_id"),)
#     cocktail_id = int
#     garnish_id = int


# class Substitute(SQLModel, table=True):
#     __tablename__ = "substitutes"
#     ingredient_id = int
#     substitute_id = int
