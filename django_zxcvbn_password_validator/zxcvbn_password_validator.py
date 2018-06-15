from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from zxcvbn import zxcvbn


class ZxcvbnPasswordValidator(object):

    def __init__(self, min_length=1):
        self.min_length = min_length

    def validate(self, password, user=None):
        results = zxcvbn(password, user_inputs=user.__dict__)
        password_strengh = results["score"]
        if password_strengh < settings.PASSWORD_MINIMAL_STRENGH:
            comment = "{} ".format(_("Your password too guessable."))
            crack_time = results["crack_times_display"]
            offline_time = crack_time["offline_slow_hashing_1e4_per_second"]
            warn = results["feedback"]["warning"]
            advice = results["feedback"]["suggestions"]
            comment += "{} ".format(_("It would take an attacker"))
            comment += f" {offline_time} "
            comment += "{} ".format(_("to guess it at 10 000 tries per second."))
            if warn:
                comment += "{} ".format(_(f" Warning : {warn}."))
            if advice:
                comment += "{} ".format(_(f" What you can do : {advice}"))
            raise ValidationError(comment)

    def get_help_text(self):
        return "{}{}{}{}".format(
            _("Our password strength estimator is inspired by password crackers."),
            _(" We do not force you to use an arbitraty number of lower, upper,"),
            _(" numbers, symbols characters... but if we're able to crack your "),
            _(" password too easily you need to find another one.")
        )
