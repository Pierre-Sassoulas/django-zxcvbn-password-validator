import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.utils.translation import ugettext_lazy as _
from zxcvbn import zxcvbn

LOGGER = logging.getLogger(__file__)

DEFAULT_MINIMAL_STRENGH = 2


def translate_zxcvbn_text(text):
    """ This PR would make it cleaner, but it will also be very slow
    to be integrated in python-zxcvbn and we want this to work now :
    https://github.com/dropbox/zxcvbn/pull/124 """
    i18n = {
        'Use a few words, avoid common phrases': _('Use a few words, avoid common phrases'),
        'No need for symbols, digits, or uppercase letters': _('No need for symbols, digits, or uppercase letters'),
        'Add another word or two. Uncommon words are better.': _('Add another word or two. Uncommon words are better.'),
        'Straight rows of keys are easy to guess': _('Straight rows of keys are easy to guess'),
        'Short keyboard patterns are easy to guess': _('Short keyboard patterns are easy to guess'),
        'Use a longer keyboard pattern with more turns': _('Use a longer keyboard pattern with more turns'),
        'Repeats like "aaa" are easy to guess': _('Repeats like "aaa" are easy to guess'),
        'Repeats like "abcabcabc" are only slightly harder to guess than "abc"': _('Repeats like "abcabcabc" are only slightly harder to guess than "abc"'),
        'Avoid repeated words and characters': _('Avoid repeated words and characters'),
        'Sequences like abc or 6543 are easy to guess': _('Sequences like abc or 6543 are easy to guess'),
        'Avoid sequences': _('Avoid sequences'),
        'Recent years are easy to guess': _('Recent years are easy to guess'),
        'Avoid recent years': _('Avoid recent years'),
        'Avoid years that are associated with you': _('Avoid years that are associated with you'),
        'Dates are often easy to guess': _('Dates are often easy to guess'),
        'Avoid dates and years that are associated with you': _('Avoid dates and years that are associated with you'),
        'This is a top-10 common password': _('This is a top-10 common password'),
        'This is a top-100 common password': _('This is a top-100 common password'),
        'This is a very common password': _('This is a very common password'),
        'This is similar to a commonly used password': _('This is similar to a commonly used password'),
        'A word by itself is easy to guess': _('A word by itself is easy to guess'),
        'Names and surnames by themselves are easy to guess': _('Names and surnames by themselves are easy to guess'),
        'Common names and surnames are easy to guess': _('Common names and surnames are easy to guess'),
        'Capitalization doesn\'t help very much': _('Capitalization doesn\'t help very much'),
        'All-uppercase is almost as easy to guess as all-lowercase': _('All-uppercase is almost as easy to guess as all-lowercase'),
        'Reversed words aren\'t much harder to guess': _('Reversed words aren\'t much harder to guess'),
        'Predictable substitutions like \'@\' instead of \'a\' don\'t help very much': _('Predictable substitutions like \'@\' instead of \'a\' don\'t help very much'),
    }
    translated_text = i18n.get(text)
    if translated_text is None:
        # zxcvbn is inconsistent, sometime there is a dot, sometime not
        translated_text = i18n.get(text[:-1])
    if translated_text is None:
        LOGGER.warning(f"No translation for '{text}' or '{text[:-1]}', update the generatei18ndict command, please.")
        return text
    return translated_text


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
                return f"{comment}- {translate_zxcvbn_text(advices)}"
            for advice in advices:
                comment += f"- {translate_zxcvbn_text(advice)}\n"
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
            4: _("without a dedicated team and an access to our database.")
        }
        expectations += " {}".format(hardness.get(self.password_minimal_strengh))
        return "{} {} {} {}".format(
            _("There is no specific rule for a great password,"),
            _("however if your password is too easy to guess,"),
            _("we will tell you how to make a better one."),
            expectations
        )
