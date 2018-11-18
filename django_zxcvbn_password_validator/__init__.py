""" A password validator for django, based on zxcvbn-python. """

from django_zxcvbn_password_validator.settings import DEFAULT_MINIMAL_STRENGH
from django_zxcvbn_password_validator.zxcvbn_password_validator import (
    ZxcvbnPasswordValidator,
)

__all__ = ["ZxcvbnPasswordValidator", "DEFAULT_MINIMAL_STRENGH"]
