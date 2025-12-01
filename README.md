# django-zxcvbn-password-validator

A translatable password validator for django, based on zxcvbn-python and available with
pip.

Professional support for django-zxcvbn-password-validator is available as part of the
[Tidelift Subscription](https://tidelift.com/subscription/pkg/pypi-django-zxcvbn-password-validator?utm_source=pypi-django-zxcvbn-password-validator&utm_medium=referral&utm_campaign=enterprise)

[![Build status](https://github.com/Pierre-Sassoulas/django-zxcvbn-password-validator/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/Pierre-Sassoulas/django-zxcvbn-password-validator/actions?branch=main)
[![Coverage Status](https://coveralls.io/repos/github/Pierre-Sassoulas/django-zxcvbn-password-validator/badge.svg?branch=master)](https://coveralls.io/github/Pierre-Sassoulas/django-zxcvbn-password-validator?branch=master)
[![PyPI version](https://badge.fury.io/py/django-zxcvbn-password-validator.svg)](https://badge.fury.io/py/django-zxcvbn-password-validator)
[![Published on Django Packages](https://img.shields.io/badge/Published%20on-Django%20Packages-0c3c26)](https://djangopackages.org/packages/p/django-zxcvbn-password-validator/)

## Translating the project

This project is available in multiple language. Your contribution would be very
appreciated if you know a language that is not yet available. See
[how to contribute](CONTRIBUTING.md)

### Language available

The software is developed in English. Other available languages are:

[![Translation status](https://hosted.weblate.org/widget/django-zxcvbn-password-validator/multi-auto.svg)](https://hosted.weblate.org/engage/django-zxcvbn-password-validator/)

- [x] Arabic thanks to Claude AI Assistant
- [x] Armenian thanks to Claude AI Assistant
- [x] Brazilian Portuguese thanks to [Andrés Martano](https://github.com/andresmrm/) and
      Claude AI Assistant (corrections)
- [x] Chinese Simplified thanks to Claude AI Assistant
- [x] Czech thanks to [Michal Čihař](https://github.com/nijel/)
- [x] Dutch thanks to [Thom Wiggers](https://github.com/thomwiggers/)
- [x] English
- [x] French thanks to [Pierre Sassoulas](https://github.com/Pierre-Sassoulas/) and
      [Lionel Sausin](https://github.com/ls-initiatives)
- [x] German thanks to Claude AI Assistant
- [x] Hausa thanks to Claude AI Assistant
- [x] Hindi thanks to Claude AI Assistant
- [x] Hungarian thanks to [RViktor](https://github.com/rviktor/)
- [x] Indonesian thanks to Claude AI Assistant
- [x] Italian thanks to Claude AI Assistant
- [x] Japanese thanks to Claude AI Assistant
- [x] Korean thanks to Claude AI Assistant
- [x] Polish thanks to Claude AI Assistant
- [x] Portuguese thanks to Claude AI Assistant
- [x] Russian thanks to Claude AI Assistant
- [x] Spanish thanks to Claude AI Assistant
- [x] Swahili thanks to Claude AI Assistant
- [x] Thai thanks to Claude AI Assistant
- [x] Turkish thanks to Claude AI Assistant
- [x] Ukrainian thanks to Claude AI Assistant
- [x] Vietnamese thanks to Claude AI Assistant
- [x] Yoruba thanks to Claude AI Assistant

## Creating a user with django-zxcvbn-password-validator

If the password is not strong enough, we provide errors explaining what you need to do :

![English example](doc/english_example.png "English example")

The error message are translated to your target language (even the string given by
zxcvbn that are in english only) :

![Translated example](doc/french_example.png "Translated example")

## How to use

Add `django-zxcvbn-password-validator` to your requirements and get it with pip. Then
everything happens in your settings file.

Add `'django_zxcvbn_password_validator'` in the `INSTALLED_APPS` :

```python
INSTALLED_APPS = [
    # ...
    "django_zxcvbn_password_validator"
]
```

Modify `AUTH_PASSWORD_VALIDATORS` :

```python
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django_zxcvbn_password_validator.ZxcvbnPasswordValidator",
    },
    # ...
]
```

You could choose to use zxcvbn alone, but I personally still use Django's
`UserAttributeSimilarityValidator`, because there seems to be still be some problem with
it integrating user information with zxcvbn (as of june 2018).

Finally, you can set the `PASSWORD_MINIMAL_STRENGTH` to your liking (default is 2),
every password scoring lower than this number will be rejected :

```python
# 0 too guessable: risky password. (guesses < 10^3)
# 1 very guessable: protection from throttled online attacks.
# (guesses < 10^6)
# 2 somewhat guessable: protection from unthrottled online attacks.
# (guesses < 10^8)
# 3 safely unguessable: moderate protection from offline slow-hash scenario.
# (guesses < 10^10)
# 4 very unguessable: strong protection from offline slow-hash scenario.
# (guesses >= 10^10)
PASSWORD_MINIMAL_STRENGTH = 0 if DEBUG else 4
```
