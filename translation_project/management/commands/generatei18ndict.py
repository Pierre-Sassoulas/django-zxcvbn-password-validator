from django.core.management.base import BaseCommand

from django_zxcvbn_password_validator.translate_zxcvbn_text import (
    zxcvbn_feedback_strings,
)


class Command(BaseCommand):
    help = "Generate the ZXCVBN_I18N dict for the translate_zxcvbn_text module."

    def handle(self, *args, **options):
        lines = ["ZXCVBN_I18N = {"]
        # zxcvbn is inconsistent about trailing dots; translate_zxcvbn_text
        # also matches on the dot-stripped key, so we strip here to keep keys
        # stable and avoid duplicates that differ only by a trailing ".".
        messages = sorted(
            {message.rstrip(".") for message in zxcvbn_feedback_strings()}
        )
        for message in messages:
            # Pick a quote style that does not clash with the message content.
            quote = '"' if "'" in message and '"' not in message else "'"
            literal = f"{quote}{message}{quote}"
            lines.append(f"    {literal}: _({literal}),")
        lines.append("}")
        self.stdout.write("\n".join(lines))
        self.stdout.write(
            "\nCopy the dict above into translate_zxcvbn_text.py, "
            "then run 'python manage.py makemessages'."
        )
