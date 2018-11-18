import logging

from django.utils.translation import ugettext_lazy as _

LOGGER = logging.getLogger(__file__)


def translate_zxcvbn_text(text):
    """ This PR would make it cleaner, but it will also be very slow
    to be integrated in python-zxcvbn and we want this to work now :
    https://github.com/dropbox/zxcvbn/pull/124 """
    i18n = {
        "Use a few words, avoid common phrases": _(
            "Use a few words, avoid common phrases"
        ),
        "No need for symbols, digits, or uppercase letters": _(
            "No need for symbols, digits, or uppercase letters"
        ),
        "Add another word or two. Uncommon words are better.": _(
            "Add another word or two. Uncommon words are better."
        ),
        "Straight rows of keys are easy to guess": _(
            "Straight rows of keys are easy to guess"
        ),
        "Short keyboard patterns are easy to guess": _(
            "Short keyboard patterns are easy to guess"
        ),
        "Use a longer keyboard pattern with more turns": _(
            "Use a longer keyboard pattern with more turns"
        ),
        'Repeats like "aaa" are easy to guess': _(
            'Repeats like "aaa" are easy to guess'
        ),
        'Repeats like "abcabcabc" are only slightly harder to guess than "abc"': _(
            'Repeats like "abcabcabc" are only slightly harder to guess than "abc"'
        ),
        "Avoid repeated words and characters": _("Avoid repeated words and characters"),
        'Sequences like "abc" or "6543" are easy to guess': _(
            'Sequences like "abc" or "6543" are easy to guess'
        ),
        "Avoid sequences": _("Avoid sequences"),
        "Recent years are easy to guess": _("Recent years are easy to guess"),
        "Avoid recent years": _("Avoid recent years"),
        "Avoid years that are associated with you": _(
            "Avoid years that are associated with you"
        ),
        "Dates are often easy to guess": _("Dates are often easy to guess"),
        "Avoid dates and years that are associated with you": _(
            "Avoid dates and years that are associated with you"
        ),
        "This is a top-10 common password": _("This is a top-10 common password"),
        "This is a top-100 common password": _("This is a top-100 common password"),
        "This is a very common password": _("This is a very common password"),
        "This is similar to a commonly used password": _(
            "This is similar to a commonly used password"
        ),
        "A word by itself is easy to guess": _("A word by itself is easy to guess"),
        "Names and surnames by themselves are easy to guess": _(
            "Names and surnames by themselves are easy to guess"
        ),
        "Common names and surnames are easy to guess": _(
            "Common names and surnames are easy to guess"
        ),
        "Capitalization doesn't help very much": _(
            "Capitalization doesn't help very much"
        ),
        "All-uppercase is almost as easy to guess as all-lowercase": _(
            "All-uppercase is almost as easy to guess as all-lowercase"
        ),
        "Reversed words aren't much harder to guess": _(
            "Reversed words aren't much harder to guess"
        ),
        "Predictable substitutions like '@' instead of 'a' don't help very much": _(
            "Predictable substitutions like '@' instead of 'a' don't help very much"
        ),
    }
    translated_text = i18n.get(text)
    if translated_text is None:
        # zxcvbn is inconsistent, sometime there is a dot, sometime not
        translated_text = i18n.get(text[:-1])
    if translated_text is None:
        LOGGER.warning(
            "No translation for '%s' or '%s', update the generatei18ndict command.",
            text,
            text[:-1],
        )
        return text
    return translated_text


def translate_zxcvbn_time_estimate(text):
    def replace_dict(text, times):
        for original, translated in times.items():
            text = text.replace(original, str(translated))
        return text

    if text == "less than a second":
        return _("less than a second")
    text = text.replace("centuries", str(_("centuries")))
    plural_times = {
        "seconds": _("seconds"),
        "minutes": _("minutes"),
        "hours": _("hours"),
        "days": _("days"),
        "months": _("months"),
        "years": _("years"),
    }
    times = {
        "second": _("second"),
        "minute": _("minute"),
        "hour": _("hour"),
        "day": _("day"),
        "month": _("month"),
        "year": _("year"),
    }
    # Plural first to avoid replacing "hours" by _("hour") + s
    # Adding an 's' does not mean plural in every language
    text = replace_dict(text, plural_times)
    text = replace_dict(text, times)
    return text
