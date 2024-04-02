from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized


class AuthorRegisterFormUniTest(TestCase):
    @parameterized.expand([
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('first_name', 'Name'),
        ('last_name', 'Last Name'),
        ('password', 'Password'),
        ('confirm_password', 'Confirm your Password'),
    ])
    def test_fields_help_text(self, field, placeholder):
        form = RegisterForm()
        current = form[field].field.widget.attrs.get('placeholder')
        self.assertEqual(placeholder, current)

    @parameterized.expand([
        ('username', 'Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.'), # noqa E501
        ('email', 'The e-mail must be valid.'),
        ('password', 'Password must have at least one uppercase letter,  one lowercase letter and one number. The length should be at least 8 characters.'), # noqa E501
    ])
    def test_fields_placeholder(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(needed, current)

    @parameterized.expand([
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('first_name', 'Name'),
        ('last_name', 'Last Name'),
        ('password', 'Password'),
        ('confirm_password', 'Confirm Password'),
    ])
    def test_fields_labels(self, field, placeholder):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(placeholder, current)
