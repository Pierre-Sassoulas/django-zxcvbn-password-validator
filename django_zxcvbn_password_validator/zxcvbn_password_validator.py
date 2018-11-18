from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.utils.translation import ugettext_lazy as _
from zxcvbn import zxcvbn

from django_zxcvbn_password_validator.settings import DEFAULT_MINIMAL_STRENGH
from django_zxcvbn_password_validator.translate_zxcvbn_text import (
    translate_zxcvbn_text,
    translate_zxcvbn_time_estimate,
)


class ZxcvbnPasswordValidator:
    def __init__(self, min_length=1):
        self.min_length = min_length
        self.password_minimal_strengh = getattr(
            settings, "PASSWORD_MINIMAL_STRENGH", DEFAULT_MINIMAL_STRENGH
        )
        self.__check_password_minimal_strengh()

    def __check_password_minimal_strengh(self):
        error_msg = "ZxcvbnPasswordValidator need an integer between 0 and 4 "
        error_msg += "for PASSWORD_MINIMAL_STRENGH in the settings."
        if int(self.password_minimal_strengh) != self.password_minimal_strengh:
            error_msg += f" (not a {self.password_minimal_strengh.__class__.__name__})"
            raise ImproperlyConfigured(error_msg)
        if self.password_minimal_strengh < 0 or self.password_minimal_strengh > 4:
            error_msg += f" ({self.password_minimal_strengh} is not in [0,4])"
            raise ImproperlyConfigured(error_msg)

    def validate(self, password, user=None):
        def add_list_of_advices(header, comments, advices):
            if isinstance(advices, str):
                comments.append(f"{header} : {translate_zxcvbn_text(advices)}")
            else:
                for advice in advices:
                    comments.append(f"{header} : {translate_zxcvbn_text(advice)}")
            return comments

        user_imputs = []
        if user:
            for value in user.__dict__.values():
                user_imputs.append(value)
        results = zxcvbn(password, user_inputs=user_imputs)
        password_strengh = results["score"]
        if password_strengh < self.password_minimal_strengh:
            crack_time = results["crack_times_display"]
            offline_time = crack_time["offline_slow_hashing_1e4_per_second"]
            warnings = results["feedback"]["warning"]
            advices = results["feedback"]["suggestions"]
            comments = []
            comments.append(
                "{} {}".format(
                    _("Your password is too guessable :"),
                    _("It would take an offline attacker %(time)s to guess it.")
                    % {"time": translate_zxcvbn_time_estimate(offline_time)},
                )
            )
            if warnings:
                comments = add_list_of_advices(_("Warning"), comments, warnings)
            if advices:
                comments = add_list_of_advices(_("Advice"), comments, advices)
            raise ValidationError(comments)

    def get_help_text(self):
        expectations = _("We expect")
        if self.password_minimal_strengh == 0:
            expectations += " {}".format(
                _("nothing: you can use any password you want.")
            )
            return expectations
        expectations += " {}".format(_("a password that cannot be guessed"))
        hardness = {
            1: _("by your familly or friends."),
            2: _("by attackers online."),
            3: _("without access to our database."),
            4: _("without a dedicated team and an access to our database."),
        }
        expectations += " {}".format(hardness.get(self.password_minimal_strengh))
        return "{} {} {} {}".format(
            _("There is no specific rule for a great password,"),
            _("however if your password is too easy to guess,"),
            _("we will tell you how to make a better one."),
            expectations,
        )
