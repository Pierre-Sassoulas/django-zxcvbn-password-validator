from django.contrib.auth.models import User
from django.contrib.auth.password_validation import get_default_password_validators
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from django_zxcvbn_password_validator.zxcvbn_password_validator import ZxcvbnPasswordValidator, DEFAULT_MINIMAL_STRENGH
from django.conf import settings
from django.core.exceptions import ValidationError, ImproperlyConfigured

@override_settings(AUTH_PASSWORD_VALIDATORS=[
    {
        'NAME': 'django_zxcvbn_password_validator.ZxcvbnPasswordValidator',
    },
])
class ZxcvbnPasswordValidatorTest(TestCase):

    def setUp(self):
        self.validator = get_default_password_validators()[0]
        self.maxDiff = None

    def test_password_minimal_strengh_not_set(self):
        del settings.PASSWORD_MINIMAL_STRENGH
        self.validator = ZxcvbnPasswordValidator()
        self.assertEqual(self.validator.password_minimal_strengh, DEFAULT_MINIMAL_STRENGH)
        
    @override_settings(PASSWORD_MINIMAL_STRENGH="4")
    def test_password_minimal_strengh_not_int(self):
        with self.assertRaises(ImproperlyConfigured) as cm:
            self.validator = ZxcvbnPasswordValidator()
        self.assertIn("need an integer between 0 and 4", str(cm.exception))
        self.assertIn("(not a str)", str(cm.exception))

    @override_settings(PASSWORD_MINIMAL_STRENGH=5)
    def test_password_minimal_strengh_not_in_range_high(self):
        with self.assertRaises(ImproperlyConfigured) as cm:
            self.validator = ZxcvbnPasswordValidator()
        self.assertIn("need an integer between 0 and 4", str(cm.exception))

    @override_settings(PASSWORD_MINIMAL_STRENGH=-1)
    def test_password_minimal_strengh_not_in_range_low(self):
        with self.assertRaises(ImproperlyConfigured) as cm:
            self.validator = ZxcvbnPasswordValidator()
        self.assertIn("need an integer between 0 and 4", str(cm.exception))

    @override_settings(LANGUAGE_CODE='en-us')
    def test_validate_too_short(self):
        with self.assertRaises(ValidationError) as cm:
            self.validator.validate('d@1sR')
        self.assertIn('Add another word or two.', cm.exception.messages[0])
        with self.assertRaises(ValidationError) as cm:
            self.validator.validate('d5G=}78')
        self.assertIn('Add another word or two.', cm.exception.messages[0])

    @override_settings(LANGUAGE_CODE='en-us')
    @override_settings(PASSWORD_MINIMAL_STRENGH=4)
    def test_validate_user_similarity(self):
        user = User.objects.create(
            username='testclient', first_name='Test', last_name='Client',
            email='testclient@example.com',
            password='sha1$6efc0$f93efe9fd7542f25a7be94871ea45aa95de57161',
        )
        self.assertIsNone(self.validator.validate('testclient@example.com'))

        with self.assertRaises(ValidationError) as cm:
            self.validator.validate('testclient@example.com', user=user),
        self.assertIn("Your password is too guessable", cm.exception.messages[0])


    @override_settings(PASSWORD_MINIMAL_STRENGH=0)
    def test_low_password_complexity(self):
        self.validator = ZxcvbnPasswordValidator()
        self.assertIsNone(self.validator.validate('password'))
        self.assertIsNone(self.validator.validate('123'))
        self.assertIsNone(self.validator.validate('godzilla'))

    @override_settings(PASSWORD_MINIMAL_STRENGH=2)
    @override_settings(LANGUAGE_CODE='en-us')
    def test_medium_password_complexity(self):
        self.validator = ZxcvbnPasswordValidator()
        with self.assertRaises(ValidationError) as cm:
            self.assertIsNone(self.validator.validate('p@sswOrd1'))
        self.assertIn("Your password is too guessable", cm.exception.messages[0])
        self.assertIn("Predictable substitutions", cm.exception.messages[0])
        with self.assertRaises(ValidationError) as cm:
            self.assertIsNone(self.validator.validate('123123123123'))
        self.assertIn("Your password is too guessable", cm.exception.messages[0])
        self.assertIn('Repeats like "abcabcabc"', cm.exception.messages[0])
        with self.assertRaises(ValidationError) as cm:
            self.assertIsNone(self.validator.validate('g0dz1ll@'))
        self.assertIn("Your password is too guessable", cm.exception.messages[0])
        self.assertIn("- This is similar to a commonly used password.\n", cm.exception.messages[0])
 
    @override_settings(PASSWORD_MINIMAL_STRENGH=4)
    def test_high_password_complexity(self):
        self.validator = ZxcvbnPasswordValidator()
        self.assertRaises(ValidationError, self.validator.validate, 'password')
        self.assertRaises(ValidationError, self.validator.validate, '123')
        self.assertRaises(ValidationError, self.validator.validate, 'godzilla')
        self.assertIsNone(self.validator.validate('Ho, you want a better password ? This is a better password :@'))
        self.assertIsNone(self.validator.validate("123 je m'en vais au bois, 456 cueillir des cerises, 789 avec une variation quand même :)"))
        self.assertIsNone(self.validator.validate('A God, an alpha predator, Godzilla.'))

    @override_settings(LANGUAGE_CODE='en-us')
    def test_help_text(self):
        self.assertEqual(
            self.validator.get_help_text(),
            "There is no specific rule for a great password, however if your"
            " password is too easy to guess, we will tell you how to make a "
            "better one. We expect a password that cannot be guessed without"
            " access to our database."
        )

    @override_settings(LANGUAGE_CODE='en-us')
    @override_settings(PASSWORD_MINIMAL_STRENGH=0)
    def test_help_text_accept_all(self):
        self.validator = ZxcvbnPasswordValidator()
        self.assertEqual(
            self.validator.get_help_text(),
            "We expect nothing : you can use any password you want."
        )

    @override_settings(LANGUAGE_CODE='en-us')
    @override_settings(PASSWORD_MINIMAL_STRENGH=1)
    def test_help_text_low_password_complexity(self):
        self.validator = ZxcvbnPasswordValidator()
        self.assertEqual(
            self.validator.get_help_text(),
            "There is no specific rule for a great password, however if your"
            " password is too easy to guess, we will tell you how to make a "
            "better one. We expect a password that cannot be guessed by your"
            " familly or friends."
        )

    @override_settings(LANGUAGE_CODE='fr')
    @override_settings(PASSWORD_MINIMAL_STRENGH=2)
    def test_help_text_i18n(self):
        self.validator = ZxcvbnPasswordValidator()
        self.assertEqual(
            self.validator.get_help_text(),
            "Il n'y a pas de règle absolu pour un bon mot de passe, "
            "cependant si votre mot de passe est trop facile à deviner,"
            " nous vous dirons comment l'améliorer. Nous nous attendons à un "
            "mot de passe qui ne ne peut pas être deviné par des aggresseurs "
            "depuis internet."
        )
