from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Will generate what the i18n dict for the translate_zxcvbn_text function"

    def handle(self, *args, **options):
        existings_messages = [
            "Use a few words, avoid common phrases",
            "No need for symbols, digits, or uppercase letters",
            "Add another word or two. Uncommon words are better.",
            "Straight rows of keys are easy to guess",
            "Short keyboard patterns are easy to guess",
            "Use a longer keyboard pattern with more turns",
            'Repeats like "aaa" are easy to guess',
            'Repeats like "abcabcabc" are only slightly harder to guess than "abc"',
            "Avoid repeated words and characters",
            'Sequences like "abc" or "6543" are easy to guess',
            "Avoid sequences",
            "Recent years are easy to guess",
            "Avoid recent years",
            "Avoid years that are associated with you",
            "Dates are often easy to guess",
            "Avoid dates and years that are associated with you",
            "This is a top-10 common password",
            "This is a top-100 common password",
            "This is a very common password",
            "This is similar to a commonly used password",
            "A word by itself is easy to guess",
            "Names and surnames by themselves are easy to guess",
            "Common names and surnames are easy to guess",
            "Capitalization doesn't help very much",
            "All-uppercase is almost as easy to guess as all-lowercase",
            "Reversed words aren't much harder to guess",
            "Predictable substitutions like '@' instead of 'a' don't help very much",
        ]
        msg = "    i18n = {"
        for message in existings_messages:
            message = message.replace("'", "\\'")
            msg += f"        '{message}': _('{message}'),"
        msg += "    }"
        msg += "Please copy paste the following in the translate_zxcvbn_text function,"
        msg += " then use 'python manage.py makemessages'."
        print(msg)
