## Install

### Requirements

- PostgreSQL database (it could work with sqlite as well)
- Python 3.8.x

### Prepare environment file

Copy example of environment configuration:
```shell
$ cp warehouse/warehouse/.env.example warehouse/warehouse/.env
```
Set correct settings within `warehouse/warehouse/.env` file. It is important to keep`ATOMIC_REQUESTS=True` being set to 
true check https://docs.djangoproject.com/en/3.1/topics/db/transactions/#tying-transactions-to-http-requests for details.

Django `SECRET_KEY` could be generated with the following command:

```shell
$  python manage.py generate_secret_key
```

### Prepare environment and install dependencies
Project uses https://github.com/jazzband/pip-tools to build predictable and deterministic dependencies for both 
production and development.
```shell
$ python -m venv venv
$ pip install -r requirements-dev.txt
```

### Run migrations 

```shell
$ cd warehouse
$ python manage.py migrate
```

### Run project 
```shell
$ make run
```

### Next steps, improvement areas & ideas
- Optimisation of the statistics overview endpoint
- Introduce pagination for lists of products, batches and distributions
- Assess index usage and potential performance
- Clean codebase from unused elements (middlewares, django applications etc)
- Increase test coverage ( check results of `make coverage` html report)
- Have better docstrings or enforce that with linting tools
- Cover code with type annotations or use mypy (check stubs for recent versions of Django)
- Create Dockerfile
- Automate code checks, tests execution and image build with github actions or other CI/CD tools
- Add logging configuration and monitoring tools (Sentry, Datadog or Newrelic)
- Add project version management (bumpversion?)

### Screenshots

![API docs](https://www.evernote.com/shard/s46/sh/f853500b-b57e-438a-aaaf-3cc9c4158a45/d6d052221d03a072/res/7a5c89b3-fcb4-4f1a-a6ec-d61f5bc13041)
