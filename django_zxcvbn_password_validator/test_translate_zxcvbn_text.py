from django.test import TestCase, override_settings

from django_zxcvbn_password_validator.translate_zxcvbn_text import translate_zxcvbn_text


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
