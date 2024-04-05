from tests.functional_tests.authors.base_authors import AuthorsBaseTest
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_password = 'password'

        user = User.objects.create_user(
            username='user',
            password=string_password
        )

        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Username')
        password_field = self.get_by_placeholder(form, 'Password')

        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        form.submit()

        self.assertIn(
            f'You are logged in with {user.username}.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
