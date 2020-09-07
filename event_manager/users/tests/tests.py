from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from ..views import sign_up


class TestSignUp(TestCase):
    def setUp(self):
        self.client = Client()

    def test_sign_up_redirects_home(self):
        sign_up_data = {
            'username': 'newuser',
            'password1': 'itsasecret',
            'password2': 'itsasecret',
        }
        res = self.client.post(reverse('sign-up'), sign_up_data)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home'))
        user_created = User.objects.filter(username=sign_up_data['username']).exists()
        self.assertTrue(user_created)

    def test_sign_up_success_message(self):
        sign_up_data = {
            'username': 'anothernewuser',
            'password1': 'itsasecret2',
            'password2': 'itsasecret2',
        }
        res = self.client.post(reverse('sign-up'), sign_up_data, follow=True)
        self.assertEqual(res.status_code, 200)
        msg = list(res.context.get('messages'))[0]
        self.assertEqual(msg.tags, 'success')
        self.assertEqual(msg.message, f"Successfully created new account {sign_up_data['username']}!")
        user_created = User.objects.filter(username=sign_up_data['username']).exists()
        self.assertTrue(user_created)

    def test_sign_up_url(self):
        url = reverse('sign-up')
        self.assertEqual(resolve(url).func, sign_up)