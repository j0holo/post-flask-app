# How generate a secret key

```bash
python -c "import secrets;print(secrets.token_urlsafe(50))"
```

# .env sample for local testing

```bash
SECRET_KEY=secret_key
# assumes the same docker database as used for unit tests
DSN="user=postgres password=password host=localhost"
```

# Manually installed dependencies

* <b>flask</b>: the microframework web
* <b>python-dotenv</b>: python package to load .env values to environment variables

# Run unit tests

1. `docker run --rm -d -p 5432:5432 --name=postgres-flask -e POSTGRES_PASSWORD=password -e POSTGRES_DB=flask  postgres:13`
1. `pytest`
