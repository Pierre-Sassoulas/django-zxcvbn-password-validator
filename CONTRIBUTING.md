# Contributing

## Translating the project

This project is available in multiple languages. Your contribution would be very
appreciated if you know a language that is not yet available or if you want to improve
an existing translation (especially AI-generated ones).

### As a non dev

The translations can be edited online using
[Weblate](https://hosted.weblate.org/engage/django-zxcvbn-password-validator/).

### As a dev

```bash
python manage.py makemessages --locale=<desired locale>
# python manage.py migrate
# python manage.py createsuperuser ? (You need to login for rosetta)
python manage.py runserver
# Access http://localhost:8000/admin to login
# Then go to http://localhost:8000/rosetta to translate
python manage.py makemessages --no-obsolete --no-wrap
```

## Testing

```bash
python manage.py test
```

## Coverage

```bash
coverage run ./manage.py test
coverage html
# Open htmlcov/index.html in a navigator
```

## Lint

We're using `pre-commit`, it should take care of linting during commit.

```bash
pip3 install -e ".[dev]"
pre-commit install
```
