# django-zxcvbn-password-validator

A password validator for django, based on zxcvbn-python and available with pip.

[![Build Status](https://travis-ci.org/Pierre-Sassoulas/django-zxcvbn-password-validator.svg?branch=master)](https://travis-ci.org/Pierre-Sassoulas/django-zxcvbn-password-validator)
[![Coverage Status](https://coveralls.io/repos/github/Pierre-Sassoulas/django-zxcvbn-password-validator/badge.svg?branch=master)](https://coveralls.io/github/Pierre-Sassoulas/django-zxcvbn-password-validator?branch=master)
[![PyPI version](https://badge.fury.io/py/django-zxcvbn-password-validator.svg)](https://badge.fury.io/py/django-zxcvbn-password-validator)

# How to use

Add it to your requirements and get it with pip.

	django-zxcvbn-password-validator

Then everything happens in your settings file.

Add `'django_zxcvbn_password_validator'` in the `INSTALLED_APPS` :

	INSTALLED_APPS = [
		...
		'django_zxcvbn_password_validator'
	]

Modify `AUTH_PASSWORD_VALIDATORS` :

	AUTH_PASSWORD_VALIDATORS = [
		{
			'NAME': 'django_zxcvbn_password_validator.ZxcvbnPasswordValidator',
		},
		...
	]

You could choose to use zxcvbn alone, but I personally still use Django's `UserAttributeSimilarityValidator`,
because there seems to be still be some problem with it integrating user informations with zxcvbn (as of june 2018).

Finally you can set the `PASSWORD_MINIMAL_STRENGH` to your liking (default is 2),
every password scoring lower than this number will be rejected :

	# 0 too guessable: risky password. (guesses < 10^3)
	# 1 very guessable: protection from throttled online attacks. (guesses < 10^6)
	# 2 somewhat guessable: protection from unthrottled online attacks. (guesses < 10^8)
	# 3 safely unguessable: moderate protection from offline slow-hash scenario. (guesses < 10^10)
	# 4 very unguessable: strong protection from offline slow-hash scenario. (guesses >= 10^10)
