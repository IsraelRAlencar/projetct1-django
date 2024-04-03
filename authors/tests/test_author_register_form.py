from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse


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
        ('username', 'Required. Length between 4 and 40 characters. Letters, numbers and @.+-_ only.' ), # noqa E501
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


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'Username',
            'email': 'email@gmail.com',
            'first_name': 'Name',
            'last_name': 'LastName',
            'password': 'Password@01',
            'confirm_password': 'Password@01'
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('email', 'E-mail is required'),
        ('first_name', 'Write your name'),
        ('last_name', 'Write your last name'),
        ('password', 'Password must not be empty'),
        ('confirm_password', 'Repeat your password'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, self.form_data, follow=True)

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'Usr'
        url = reverse('authors:create')
        response = self.client.post(url, self.form_data, follow=True)

        msg = 'Username must have at least 4 characters'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username')) # noqa E501

    def test_username_field_max_lenght_should_be_40(self):
        self.form_data['username'] = 'U' * 41
        url = reverse('authors:create')
        response = self.client.post(url, self.form_data, follow=True)

        msg = 'Username must have a max of 40 characters'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username')) # noqa E501

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:create')
        response = self.client.post(url, self.form_data, follow=True)

        msg = 'Password must have at least one uppercase letter, one lowercase letter and one number. The length should be at least 8 characters.' # noqa E501
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password')) # noqa E501

        self.form_data['password'] = '@A123abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.context['form'].errors.get('password'))

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = '@A123abc123'
        self.form_data['confirm_password'] = '@A123abc1234'
        url = reverse('authors:create')
        response = self.client.post(url, self.form_data, follow=True)

        msg = 'Passwords do not match.'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('confirm_password')) # noqa E501

        self.form_data['password'] = '@A123abc123'
        self.form_data['confirm_password'] = '@A123abc123'
        url = reverse('authors:create')
        response = self.client.post(url, self.form_data, follow=True)

        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:create')
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

    def test_email_field_must_be_unique(self):
        url = reverse('authors:create')
        self.client.post(url, data=self.form_data, follow=True)

        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'User e-mail is already registered.'
        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))
