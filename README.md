# django-zxcvbn-password-validator

A translatable password validator for django, based on zxcvbn-python and available with
pip.

Unlike rule-based validators (minimum length, must contain a digit...), zxcvbn estimates
actual password strength using pattern matching, common password dictionaries, and
keyboard layout analysis. It provides meaningful, actionable feedback to help users
create stronger passwords.

Professional support for django-zxcvbn-password-validator is available as part of the
[Tidelift Subscription](https://tidelift.com/subscription/pkg/pypi-django-zxcvbn-password-validator?utm_source=pypi-django-zxcvbn-password-validator&utm_medium=referral&utm_campaign=enterprise)

[![Build status](https://github.com/Pierre-Sassoulas/django-zxcvbn-password-validator/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/Pierre-Sassoulas/django-zxcvbn-password-validator/actions?branch=main)
[![Coverage Status](https://coveralls.io/repos/github/Pierre-Sassoulas/django-zxcvbn-password-validator/badge.svg?branch=master)](https://coveralls.io/github/Pierre-Sassoulas/django-zxcvbn-password-validator?branch=master)
[![PyPI version](https://badge.fury.io/py/django-zxcvbn-password-validator.svg)](https://badge.fury.io/py/django-zxcvbn-password-validator)
[![Published on Django Packages](https://img.shields.io/badge/Published%20on-Django%20Packages-0c3c26)](https://djangopackages.org/packages/p/django-zxcvbn-password-validator/)

## How to use

Install the package:

```bash
pip install django-zxcvbn-password-validator
```

Add `'django_zxcvbn_password_validator'` in the `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "django_zxcvbn_password_validator"
]
```

Modify `AUTH_PASSWORD_VALIDATORS`:

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

You could choose to use zxcvbn alone, but using it alongside Django's
`UserAttributeSimilarityValidator` is recommended.

Finally, you can set the `PASSWORD_MINIMAL_STRENGTH` to your liking (default is 2),
every password scoring lower than this number will be rejected:

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

You can also provide a project-specific list of terms a password should not resemble
(your company name, product name, etc.) with `PASSWORD_EXTRA_DICTIONARY`. These are fed
to zxcvbn on every check, in addition to the user's own attributes:

```python
PASSWORD_EXTRA_DICTIONARY = ["AcmeCorp", "RocketWidget"]
```

If the password is not strong enough, we provide errors explaining what you need to do:

![English example](doc/english_example.png "English example")

The error messages are translated to your target language (even the strings given by
zxcvbn that are in English only):

![Translated example](doc/french_example.png "Translated example")

## Checking strength without raising

`validate()` raises a `ValidationError` when a password is too weak, which is what
Django's auth machinery expects. If you instead want to _inspect_ a password's strength
— for example to power a live strength meter — use `get_strength()`, which never raises
for a weak password:

```python
from django_zxcvbn_password_validator import ZxcvbnPasswordValidator

strength = ZxcvbnPasswordValidator().get_strength("p@sswOrd1", user=request.user)
# {
#     "score": 1,                  # zxcvbn score, 0 (worst) to 4 (best)
#     "minimal_strength": 4,       # your PASSWORD_MINIMAL_STRENGTH
#     "acceptable": False,         # score >= minimal_strength
#     "crack_time_seconds": 2.0,   # estimated offline crack time
#     "crack_time_display": "2 seconds",          # the same, translated
#     "warning": "This is similar to a commonly used password",  # translated
#     "suggestions": ["Add another word or two. Uncommon words are better"],  # translated
# }
```

The `warning`, `suggestions` and `crack_time_display` fields are translated to the
active language, just like the validation errors. `get_strength()` still raises
`ValidationError` if the password exceeds zxcvbn's maximal length.

## Compatibility

Requires Django 2+ and Python 3.6+. Note that Python 3.6 and 3.7 are not tested in CI
anymore (GitHub Actions no longer provides runners for them), so while they should work,
there is no guarantee.

## Translating the project

This project is available in 131 languages. Your contribution would be very appreciated
if you know a language that is not yet available or if you want to improve an existing
translation (especially AI-generated ones). See [how to contribute](CONTRIBUTING.md)

[![Translation status](https://hosted.weblate.org/widget/django-zxcvbn-password-validator/multi-auto.svg)](https://hosted.weblate.org/engage/django-zxcvbn-password-validator/)

<details>
<summary>Translators</summary>

- [Andrés Martano](https://github.com/andresmrm/): Brazilian Portuguese
- [eruedin](https://github.com/eruedin): Lingala
- [itsmechinmoy](https://github.com/itsmechinmoy): Assamese
- [Lionel Sausin](https://github.com/ls-initiatives): French
- [Michal Čihař](https://github.com/nijel/): Czech
- [Pierre Sassoulas](https://github.com/Pierre-Sassoulas/): French
- [RViktor](https://github.com/rviktor/): Hungarian
- [Thom Wiggers](https://github.com/thomwiggers/): Dutch
- Unai Loidi: Basque
- Claude AI: Afrikaans, Akan, Albanian, Amharic, Arabic, Armenian, Assamese,
  Azerbaijani, Belarusian, Bengali, Bosnian, Brazilian Portuguese (corrections), Breton,
  Bulgarian, Burmese, Cantonese, Catalan, Cebuano, Chichewa, Chinese Simplified, Chinese
  Traditional, Corsican, Croatian, Danish, Esperanto, Estonian, Ewe, Faroese, Filipino,
  Finnish, Fulah, Galician, Georgian, German, Greek, Gujarati, Hausa, Hawaiian, Hebrew,
  Hindi, Icelandic, Igbo, Indonesian, Irish, Italian, Japanese, Javanese, Kannada,
  Kazakh, Khmer, Kinyarwanda, Kirundi, Korean, Kurdish, Kyrgyz, Lao, Latin, Latvian,
  Lingala, Lithuanian, Luganda, Luxembourgish, Macedonian, Malagasy, Malay, Malayalam,
  Maltese, Maori, Marathi, Mongolian, Nepali, Northern Ndebele, Northern Sami, Norwegian
  Bokmål, Occitan, Odia, Oromo, Pashto, Persian, Polish, Portuguese, Punjabi, Romanian,
  Russian, Samoan, Sango, Sardinian, Scottish Gaelic, Serbian, Sesotho, Shona, Sindhi,
  Sinhala, Slovak, Slovenian, Somali, Southern Ndebele, Spanish, Sundanese, Swahili,
  Swati, Swedish, Tajik, Tamil, Telugu, Thai, Tibetan, Tigrinya, Tongan, Tsonga, Tswana,
  Turkish, Turkmen, Twi, Ukrainian, Urdu, Uzbek, Venda, Vietnamese, Welsh, Western
  Frisian, Wolof, Xhosa, Yiddish, Yoruba, Zulu

</details>
