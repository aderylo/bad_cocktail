# bad_cocktail

## Setup

### Data

This project uses PostgreSQL database data on "db" database.

### Dependencies

You need to install PostgreSQL to your local OS, or be able to access remote postgres instance.

Please provide env variables to your postgres connection.

### Installation

```shell
pip install -r requirements.txt
```

### Pre-commit hooks

Pre-commit hooks configuration has been added to the repository.
Requirements are in the `requirements.txt`.
After the requirements are installed, run `pre-commit install`. Then, pre-commit hooks should work for the repository.

### Env vars

You need to set `POSTGRES_USER`, `POSTGRES_PWD` and "`POSTGRES_HOST`" environment variables.

### Running on students(mimuw) with cgi

Set up virtual enviorment inside "public_html" directory.
Then, clone

When running on students, on can use public db and server with following credentials
placed in .env file:

```shell
POSTGRES_USER=scott
POSTGRES_PWD=tiger
POSTGRES_HOST=lkdb
```
