# mypy: ignore-errors

from django.test import TestCase, override_settings

from django_zxcvbn_password_validator.translate_zxcvbn_text import (
    ZXCVBN_I18N,
    translate_zxcvbn_text,
    zxcvbn_feedback_strings,
)


class TranslateZxcvbnTextTest(TestCase):
    @override_settings(LANGUAGE_CODE="en-us")
    def test_help_text(self):
        test = "Disregard this logging text :)."
        self.assertEqual(translate_zxcvbn_text(test), test)

    @override_settings(LANGUAGE_CODE="fr")
    def test_help_text_i18n(self):
        self.assertEqual(
            translate_zxcvbn_text("Use a few words, avoid common phrases"),
            "Utilisez quelques mots, évitez les mots souvent utilisés ensemble",
        )

    def test_dict_covers_all_zxcvbn_feedback(self):
        """Every zxcvbn feedback string must be translatable.

        Guards against drift: when a zxcvbn upgrade adds or edits a message,
        this fails in CI instead of silently falling back to English in prod.
        If it fails, run ``python manage.py generatei18ndict``, update
        ``ZXCVBN_I18N`` in translate_zxcvbn_text.py, then ``makemessages``.
        """
        missing = [
            string
            for string in zxcvbn_feedback_strings()
            # translate_zxcvbn_text also matches with the trailing "." stripped,
            # because zxcvbn is inconsistent about it.
            if string not in ZXCVBN_I18N and string[:-1] not in ZXCVBN_I18N
        ]
        self.assertEqual(
            missing,
            [],
            f"zxcvbn feedback strings not in ZXCVBN_I18N: {missing}",
        )
