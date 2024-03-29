# Buddy Recommender API

## About

A recommender service for Assistive Technology (AT), developed in the context of the [Buddy Project](https://www.buddyproject.eu/).

The Buddy Recommender API accepts numeric user-item ratings in a five-level [Likert scale](https://en.wikipedia.org/wiki/Likert_scale). Clients may additionally request for item recommendations for a given user.

## Endpoints

The Buddy Recommender API is documented with [Swagger UI](https://swagger.io/tools/swagger-ui/). Available endpoints can be visualized just by navigating to the root path of the application with any Web browser.

For example, to see the API documentation locally go to http://127.0.0.1:5000/. This also allows you to consume the API directly on the browser.

## Database Migrations

Before running the application, a database must be created. To generate the initial SQLite database, run:

```console
(venv) user@host:~$ python src/manage.py db upgrade
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 866d7a6604a8, initial migration
INFO  [alembic.runtime.migration] Running upgrade 866d7a6604a8 -> ac846ff86f07, add auth-related tables
```

## Test

To run all unit tests, execute the `test` CLI command:

```console
(venv) user@host:~$ cd src/
(venv) user@host:~$ python manage.py test
[...]
Ran 23 tests in 11.015s

OK
```

## Run

- Using the built-in Flask development server:

```console
(venv) user@host:~$ export FLASK_ENV=development
(venv) user@host:~$ python src/manage.py run
 * Serving Flask app 'manage.py' (lazy loading)
 * Environment: development
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

- In production, using `uWSGI` on top of `nginx`:

```console
(venv) user@host:~$ cd src/
(venv) user@host:~$ uwsgi wsgi.ini -w wsgi:app
[...]
WSGI app 0 (mountpoint='') ready in 0 seconds on interpreter 0x5627df2557e0 pid: 30419 (default app)
[...]
```

- In production, with Docker:

```console
user@host:~$ cd src/
user@host:~$ docker build . -t buddy-api && docker run -p 8081:5000 buddy-api
Sending build context to Docker daemon  198.1kB
Step 1/15 : FROM python:3
[...]
WSGI app 0 (mountpoint='') ready in 1 seconds on interpreter 0x55e5d20240b0 pid: 1 (default app)
[...]
*** uWSGI is running in multiple interpreter mode ***
spawned uWSGI master process (pid: 1)
spawned uWSGI worker 5 (pid: 15, cores: 1)
```
