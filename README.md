# How generate a secret key

```bash
python -c "import secrets;print(secrets.token_urlsafe(50))"
```

# .env sample

```bash
SECRET_KEY=secret_key
DATABASE_URL=postgresql://[user]:[password]@[host]:[port]/[dbname]
```

# Manually installed dependencies

* <b>flask</b>: the microframework web
* <b>python-dotenv</b>: python package to load .env values to environment variables
* <b>flask-sqlalchemy</b>: ORM for flask
* <b>Flask-Migrate</b>: "Flask-Migrate, uses Alembic which is a light Database migration tool. It helps us to Create/Update Databases and Tables. It also allows us to update an existing Table incase you delete or create new Table Fields."

# Setup database

1. python db init
2. python db migrate
3. python db upgrade