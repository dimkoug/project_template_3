import datetime
from django.urls import reverse
from django.test import TestCase, Client


# Create your tests here.

class UserSignInTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_register_returns_correct_html(self):
        sign_in_url = reverse('signup')
        self.client.get(sign_in_url)
        self.assertTemplateUsed('registration/signup.html')


    def test_user_register_invalid_date(self):
        data = {
            'birth_date': datetime.datetime.now(),
            'email': 'd@f.com',
            'password1': '1234',
            'password2': '1234'
        }
        sign_in_url = reverse('signup')
        response = self.client.post(sign_in_url, data)
        self.assertContains(response, 'Enter a valid date')

    def test_user_register_valid_date(self):
        data = {
            'birth_date': '2001-01-01',
            'email': 'd@f.com',
            'password1': '1234',
            'password2': '1234'
        }
        sign_in_url = reverse('signup')
        response = self.client.post(sign_in_url, data)
        self.assertRedirects(response, reverse('account_activation_sent'))

    def test_user_register_invalid_email(self):
        data = {
            'birth_date': '2001-01-01',
            'email': 'd',
            'password1': '1234',
            'password2': '1234'
        }
        sign_in_url = reverse('signup')
        response = self.client.post(sign_in_url, data)
        self.assertContains(response, 'Enter a valid email')

    def test_user_register_valid_email(self):
        data = {
            'birth_date': '2001-01-01',
            'email': 'd@f.com',
            'password1': '1234',
            'password2': '1234'
        }
        sign_in_url = reverse('signup')
        response = self.client.post(sign_in_url, data)
        self.assertRedirects(response, reverse('account_activation_sent'))
