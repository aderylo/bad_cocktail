CREATE OR REPLACE FUNCTION checkCocktailIngredientsFunc()
   RETURNS TRIGGER
   LANGUAGE PLPQSQL
   AS
$$
DECLARE
   rowcnt number;
BEGIN
    SELECT COUNT(*) INTO rowcnt FROM cocktail_ingredients WHERE cocktail_id = :NEW.cocktail_id;
    IF rowcnt = 0  THEN
        raise_application_error(-20000, 'The Cocktail must consist of at least one ingredient!');
    END IF;
END;
$$

CREATE TRIGGER checkCocktailIngredients
AFTER INSERT OR UPDATE OF cocktail_id ON cocktails
FOR EACH ROW
EXECUTE PROCEDURE checkCocktailIngredientsFunc();
