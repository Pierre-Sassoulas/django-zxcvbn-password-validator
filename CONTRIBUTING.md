# Contributing

## Getting started

```bash
git clone https://github.com/Pierre-Sassoulas/django-zxcvbn-password-validator
cd django-zxcvbn-password-validator
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

## Translating the project

This project is available in multiple languages. Your contribution would be very
appreciated if you know a language that is not yet available or if you want to improve
an existing translation (especially AI-generated ones).

### Using Weblate (no dev setup needed)

The translations can be edited online using
[Weblate](https://hosted.weblate.org/engage/django-zxcvbn-password-validator/). Changes
made on Weblate are automatically synced to the repository.

### Locally with Rosetta

```bash
python manage.py makemessages --locale=<desired locale>
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
# Access http://localhost:8000/admin to login
# Then go to http://localhost:8000/rosetta to translate
python manage.py makemessages --no-obsolete --no-wrap
```

## Testing and coverage

```bash
# Run tests
python manage.py test

# Run tests with coverage
coverage run ./manage.py test
coverage html
# Open htmlcov/index.html in a browser
```

## Lint

We use `pre-commit` which runs automatically on each commit. If a hook fails, the commit
is aborted — fix the issue and commit again.

```bash
# Run all hooks manually
pre-commit run --all-files
```

## Submitting changes

1. Create a branch from `main`
2. Make your changes and commit
3. Open a pull request against `main`
