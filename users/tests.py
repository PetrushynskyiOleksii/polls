"""Test for views of users' app."""

import jwt

from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_jwt.settings import api_settings

from main.settings import SECRET_KEY

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserViewsTest(TestCase):
    """Test for API user's views."""

    def setUp(self):
        """Pre-populate test data."""
        self.client = APIClient()

    def tearDown(self):
        """Clean-up test data."""
        del self.client

    def test_signup_login_views(self):
        """Test signup and login views."""
        data = {'username': 'testsignup',
                'email': 'test@email.com',
                'password': 'testpassword'
                }

        # Sign up
        response = self.client.post('/user/signup', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username='testsignup', email='test@email.com')
        self.assertIsNotNone(user)

        # Correct token in response
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        self.assertEqual(token, response.data.get('token'))

        # Already exist user
        response = self.client.post('/user/signup', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        # How to proper test these serializers exeptions in response?

        # Invalid email
        data['email'] = 'invalid email'
        response = self.client.post('/user/signup', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

        # Log in
        data.pop('email')
        response = self.client.post('/user/login', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('success', response.data.get('status'))

        # Correct token in response
        user = authenticate(username=data.get('username'),
                            password=data.get('password'))
        payload = jwt_payload_handler(user)
        token = jwt.encode(payload, SECRET_KEY)
        self.assertEqual(token, response.data.get('token'))

        user.delete()
