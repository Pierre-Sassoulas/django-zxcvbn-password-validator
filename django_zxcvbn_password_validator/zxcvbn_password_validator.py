from django.conf import settings
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _
from zxcvbn import zxcvbn

DEFAULT_MINIMAL_STRENGH = 2


class ZxcvbnPasswordValidator(object):

    def __init__(self, min_length=1):
        self.min_length = min_length
        error_msg = "ZxcvbnPasswordValidator need an integer between 0 and 4 "
        error_msg += "for PASSWORD_MINIMAL_STRENGH in the settings."
        try:
            self.password_minimal_strengh = settings.PASSWORD_MINIMAL_STRENGH
        except AttributeError:
            self.password_minimal_strengh = DEFAULT_MINIMAL_STRENGH
        if int(self.password_minimal_strengh) != self.password_minimal_strengh:
            error_msg += f" (not a {self.password_minimal_strengh.__class__.__name__})"
            raise ImproperlyConfigured(error_msg)
        if self.password_minimal_strengh < 0 or self.password_minimal_strengh > 4:
            error_msg += f" ({self.password_minimal_strengh} is not in [0,4])"
            raise ImproperlyConfigured(error_msg)

    def validate(self, password, user=None):

        def add_list_of_advices(header, comment, advices):
            comment += f"\n{header}\n"
            if isinstance(advices, str):
                return f"{comment}- {advices}"
            for advice in advices:
                comment += f"- {advice}\n"
                comment = comment[:-len("\n")]
            return comment

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
            comment = "{} {}".format(
                _(f'Your password is too guessable :'),
                _(f'It would take an offline attacker {offline_time} to guess it.'),
            )
            if warnings:
                comment = add_list_of_advices(_('Warning :'), comment, warnings)
            if advices:
                comment = add_list_of_advices(_(f'What you can do :'), comment, advices)
            raise ValidationError(comment)

    def get_help_text(self):
        expectations = _("We expect")
        if self.password_minimal_strengh == 0:
            expectations += " {}".format(_("nothing : you can use any password you want."))
            return  expectations
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
            expectations
        )
