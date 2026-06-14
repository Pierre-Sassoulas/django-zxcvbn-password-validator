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
        self.extra_dictionary = self.__get_extra_dictionary()

    @staticmethod
    def __get_extra_dictionary():
        extra_dictionary = getattr(settings, "PASSWORD_EXTRA_DICTIONARY", None) or []
        if not isinstance(extra_dictionary, (list, tuple)) or not all(
            isinstance(term, str) for term in extra_dictionary
        ):
            raise ImproperlyConfigured(
                "PASSWORD_EXTRA_DICTIONARY must be a list of strings (terms a "
                "password should not resemble, e.g. your company or product "
                f"name), not {extra_dictionary!r}."
            )
        return list(extra_dictionary)

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

    def _get_user_inputs(self, user):
        # Start from the project-wide extra dictionary (e.g. company or product
        # names), then add the user's meaningful string attributes. Skip
        # private attributes (e.g. Django's '_state'), the hashed password, and
        # any non-string value, none of which are useful as a dictionary of
        # terms the password should not resemble.
        user_inputs = list(self.extra_dictionary)
        if user:
            for key, value in user.__dict__.items():
                if key.startswith("_") or key == "password":
                    continue
                if isinstance(value, str) and value:
                    user_inputs.append(value)
        return user_inputs

    def _run_zxcvbn(self, password, user=None):
        try:
            return self.zxcvbn_implementation(
                password, user_inputs=self._get_user_inputs(user)
            )
        except ValueError as error:
            # zxcvbn raises ValueError only if the password is too long.
            raise ValidationError(
                _("Your password exceeds the maximal length of 72 characters.")
            ) from error

    def get_strength(self, password, user=None):
        """Return structured, translated strength information for a password.

        Unlike :meth:`validate`, this never raises for a weak password, so it
        can drive a strength meter or progressive UI. It still raises
        ``ValidationError`` if the password exceeds zxcvbn's maximal length.
        """
        results = self._run_zxcvbn(password, user)
        score = results["score"]
        offline_time = results["crack_times_seconds"][
            "offline_slow_hashing_1e4_per_second"
        ]
        warning = results["feedback"]["warning"]
        return {
            "score": score,
            "minimal_strength": self.password_minimal_strength,
            "acceptable": score >= self.password_minimal_strength,
            "crack_time_seconds": offline_time,
            "crack_time_display": str(translate_zxcvbn_time_estimate(offline_time)),
            "warning": translate_zxcvbn_text(warning) if warning else "",
            "suggestions": [
                translate_zxcvbn_text(suggestion)
                for suggestion in results["feedback"]["suggestions"]
            ],
        }

    def validate(self, password, user=None):
        def append_translated_feedback(old_feedbacks, feedback_type, new_feedbacks):
            if new_feedbacks:
                if isinstance(new_feedbacks, str):
                    new_feedbacks = [new_feedbacks]
                for new_feedback in new_feedbacks:
                    old_feedbacks.append(
                        f"{feedback_type} {translate_zxcvbn_text(new_feedback)}"
                    )

        results = self._run_zxcvbn(password, user)
        password_strength = results["score"]
        if password_strength < self.password_minimal_strength:
            crack_time = results["crack_times_seconds"]
            offline_time = crack_time["offline_slow_hashing_1e4_per_second"]

            feedbacks = [
                "{} {}".format(  # pylint: disable=consider-using-f-string
                    _("Your password is too guessable:"),
                    _("It would take an offline attacker %(time)s to guess it.")
                    % {"time": translate_zxcvbn_time_estimate(offline_time)},
                )
            ]
            append_translated_feedback(
                feedbacks, _("Warning:"), results["feedback"]["warning"]
            )
            append_translated_feedback(
                feedbacks, _("Advice:"), results["feedback"]["suggestions"]
            )
            raise ValidationError(feedbacks)

    def get_help_text(self):
        if self.password_minimal_strength == 0:
            return _("We expect nothing: you can use any password you want.")
        expectations = _("We expect a password that cannot be guessed %s")
        hardness = {
            1: _("by your familly or friends."),
            2: _("by attackers online."),
            3: _("without access to our database."),
            4: _("without a dedicated team and an access to our database."),
        }
        # pylint: disable=consider-using-f-string
        return "{} {} {} {}".format(
            _("There is no specific rule for a great password,"),
            _("however if your password is too easy to guess,"),
            _("we will tell you how to make a better one."),
            expectations % hardness.get(self.password_minimal_strength),
        )
