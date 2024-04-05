from tests.functional_tests.authors.base_authors import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest


@pytest.mark.functional_test
class AuthorsReqisterTest(AuthorsBaseTest):
    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form/div[1]'
        )

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register')
        form = self.get_form()

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('email@email.com')

        callback(form)
        return form

    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(form, 'Name')
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('Write your name', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(form, 'Last Name')
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('Write your last name', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_username_error_message(self):
        def callback(form):
            username_field = self.get_by_placeholder(form, 'Username')
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('This field must not be empty', form.text)
        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_placeholder(form, 'E-mail')
            email_field.send_keys('email@invalid')
            email_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('The e-mail must be valid.', form.text)
        self.form_field_test_with_callback(callback)

    def test_passwords_do_not_match_error_message(self):
        def callback(form):
            password1 = self.get_by_placeholder(form, 'Password')
            password2 = self.get_by_placeholder(form, 'Confirm your Password')
            password1.send_keys('P@ssw0rd')
            password2.send_keys('P@ssw0rdDifferent')
            password2.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('Passwords do not match.', form.text)
        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_successfully(self):
        self.browser.get(self.live_server_url + '/authors/register')

        form = self.get_form()

        self.get_by_placeholder(form, 'Name').send_keys('First Name')
        self.get_by_placeholder(form, 'Last Name').send_keys('Last Name')
        self.get_by_placeholder(form, 'Username').send_keys('my_username')
        self.get_by_placeholder(form, 'E-mail').send_keys('email@gmail.com')
        self.get_by_placeholder(form, 'Password').send_keys('P@ssw0rd')
        self.get_by_placeholder(form, 'Confirm your Password').send_keys('P@ssw0rd') # noqa E501

        form.submit()

        self.assertIn(
            'User created successfully!',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
