from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Cocktail(SQLModel, table=True):
    __tablename__ = "cocktails"
    id: int = Field(primary_key=True)
    name: str
    instructions: str
    category: str
    photo: Optional[str]
    glassId: int = Field(foreign_key="glassware.id")
    glass: "Glassware" = Relationship(back_populates="cocktails")


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


class Ingredient(SQLModel, table=True):
    __tablename__ = "ingredients"
    id: int = Field(primary_key=True)
    name: str
    price: Optional[int]


# class CocktailIngredient(SQLModel, table=True):
#     __tablename__ = "cocktail_ingredients"
#     __table_args__ = (UniqueConstraint("cocktail_id", "ingredient_id"),)
#     cocktail_id = int
#     ingredient_id = int


# class CocktailGarnish(SQLModel, table=True):
#     __tablename__ = "cocktail_garnishes"
#     __table_args__ = (UniqueConstraint("cocktail_id", "garnish_id"),)
#     cocktail_id = int
#     garnish_id = int


# class Substitute(SQLModel, table=True):
#     __tablename__ = "substitutes"
#     ingredient_id = int
#     substitute_id = int
