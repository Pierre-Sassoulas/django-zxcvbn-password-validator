# django-zxcvbn-password-validator

This is a custom password validator based on zxcvbn-python for easy use in Django project.

# How to use

Everything happens in your settings file.

Add `'django_zxcvbn_password_validator'` in the `INSTALLED_APPS` :

	INSTALLED_APPS = [
		...
		'django_zxcvbn_password_validator'
	]

Then modify `AUTH_PASSWORD_VALIDATORS` :

	AUTH_PASSWORD_VALIDATORS = [
		{
			'NAME': 'django_zxcvbn_password_validator.ZxcvbnPasswordValidator',
		},
		...
	]

You could choose to use zxcvbn alone but I personally still use the  Django's
`UserAttributeSimilarityValidator` validator.

Finally set the `PASSWORD_MINIMAL_STRENGH` :

	# 0 too guessable: risky password. (guesses < 10^3)
	# 1 very guessable: protection from throttled online attacks. (guesses < 10^6)
	# 2 somewhat guessable: protection from unthrottled online attacks. (guesses < 10^8)
	# 3 safely unguessable: moderate protection from offline slow-hash scenario. (guesses < 10^10)
	# 4 very unguessable: strong protection from offline slow-hash scenario. (guesses >= 10^10)
	PASSWORD_MINIMAL_STRENGH = 3

