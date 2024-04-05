from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class AuthorLogoutTest(TestCase):
    def test_user_tries_to_logout_using_get_method(self):
        User.objects.create_user(
            username='user',
            password='password'
        )

        self.client.login(username='user', password='password')

        response = self.client.get(reverse('authors:logout'), follow=True)

        self.assertIn(
            'Invalid logout request!',
            response.content.decode('utf-8')
        )

    def test_user_tries_to_logout_another_user(self):
        User.objects.create_user(
            username='user',
            password='password'
        )

        self.client.login(username='user', password='password')

        response = self.client.post(
            reverse('authors:logout'),
            follow=True,
            data={'username': 'another_user'}
        )

        self.assertIn(
            'Invalid logout user!',
            response.content.decode('utf-8')
        )

    def test_user_can_logout_successfully(self):
        User.objects.create_user(
            username='user',
            password='password'
        )

        self.client.login(username='user', password='password')

        response = self.client.post(
            reverse('authors:logout'),
            data={'username': 'user'},
            follow=True,
        )

        self.assertIn(
            'Logout successful!',
            response.content.decode('utf-8')
        )
