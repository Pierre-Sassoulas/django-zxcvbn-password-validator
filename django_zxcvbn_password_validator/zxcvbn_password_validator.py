# mypy: ignore-errors

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError

try:
    from django.utils.translation import gettext_lazy as _
except ImportError:
    from django.utils.translation import ugettext_lazy as _

from zxcvbn import zxcvbn

from django_zxcvbn_password_validator.settings import DEFAULT_MINIMAL_STRENGTH
from django_zxcvbn_password_validator.translate_zxcvbn_text import (
    translate_zxcvbn_text,
    translate_zxcvbn_time_estimate,
)


class ZxcvbnPasswordValidator:
    def __init__(self, min_length=1, zxcvbn_implementation=zxcvbn):
        self.min_length = min_length
        self.zxcvbn_implementation = zxcvbn_implementation
        password_minimal_strength = getattr(settings, "PASSWORD_MINIMAL_STRENGTH", None)
        if password_minimal_strength is None:
            # Compatibility with a typo in previous version.
            password_minimal_strength = getattr(
                settings, "PASSWORD_MINIMAL_STRENTH", None
            )
        if password_minimal_strength is None:
            password_minimal_strength = DEFAULT_MINIMAL_STRENGTH
        self.password_minimal_strength = password_minimal_strength
        self.__check_password_minimal_strength()

    def __check_password_minimal_strength(self):
        error_msg = "ZxcvbnPasswordValidator need an integer between 0 and 4 "
        error_msg += "for PASSWORD_MINIMAL_STRENGTH in the settings."
        try:
            not_an_int = (
                int(self.password_minimal_strength) != self.password_minimal_strength
            )
        except ValueError:
            not_an_int = True
        if not_an_int:
            error_msg += f" (not '{self.password_minimal_strength}', "
            error_msg += f"a {self.password_minimal_strength.__class__.__name__})"
            raise ImproperlyConfigured(error_msg)
        if self.password_minimal_strength < 0 or self.password_minimal_strength > 4:
            error_msg += f" ({self.password_minimal_strength} is not in [0,4])"
            raise ImproperlyConfigured(error_msg)

    def validate(self, password, user=None):
        def append_translated_feedback(old_feedbacks, feedback_type, new_feedbacks):
            if new_feedbacks:
                if isinstance(new_feedbacks, str):
                    new_feedbacks = [new_feedbacks]
                for new_feedback in new_feedbacks:
                    old_feedbacks.append(
                        f"{feedback_type} : {translate_zxcvbn_text(new_feedback)}"
                    )

        user_inputs = []
        if user:
            for value in user.__dict__.values():
                user_inputs.append(value)
        results = self.zxcvbn_implementation(password, user_inputs=user_inputs)
        password_strength = results["score"]
        if password_strength < self.password_minimal_strength:
            crack_time = results["crack_times_display"]
            offline_time = crack_time["offline_slow_hashing_1e4_per_second"]

            feedbacks = [
                "{} {}".format(  # pylint: disable=consider-using-f-string
                    _("Your password is too guessable :"),
                    _("It would take an offline attacker %(time)s to guess it.")
                    % {"time": translate_zxcvbn_time_estimate(offline_time)},
                )
            ]
            append_translated_feedback(
                feedbacks, _("Warning"), results["feedback"]["warning"]
            )
            append_translated_feedback(
                feedbacks, _("Advice"), results["feedback"]["suggestions"]
            )
            raise ValidationError(feedbacks)

    def get_help_text(self):
        expectations = _("We expect")
        if self.password_minimal_strength == 0:
            expectations += f" {_('nothing: you can use any password you want.')}"
            return expectations
        expectations += f" {_('a password that cannot be guessed')}"
        hardness = {
            1: _("by your familly or friends."),
            2: _("by attackers online."),
            3: _("without access to our database."),
            4: _("without a dedicated team and an access to our database."),
        }
        expectations += f" {hardness.get(self.password_minimal_strength)}"
        # pylint: disable=consider-using-f-string
        return "{} {} {} {}".format(
            _("There is no specific rule for a great password,"),
            _("however if your password is too easy to guess,"),
            _("we will tell you how to make a better one."),
            expectations,
        )
