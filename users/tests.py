"""Test for views of users' app."""

import jwt

from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_jwt.settings import api_settings

from main.settings import SECRET_KEY
from questions.models import Answer, Question

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserAuthTest(TestCase):
    """Test for API user's auth views."""

    def setUp(self):
        """Pre-populate test data."""
        self.client = APIClient()

    def tearDown(self):
        """Clean-up test data."""
        del self.client

    def test_signup_login_vote_views(self):
        """Test signup & login views."""
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


class UserVoteTest(TestCase):
    """Test for API user's votes views."""

    def setUp(self):
        """Pre-populate test data."""
        self.client = APIClient()
        self.test_quest = Question.objects.create(question='test question')
        self.test_answer = Answer.objects.create(question=self.test_quest, answer='test answer')

    def tearDown(self):
        """Clean-up test data."""
        del self.client
        del self.test_quest
        del self.test_answer

    def test_signup_login_vote_views(self):
        """Test vote views."""
        url = '/user/votefor/{}/answer/{}/'.format(self.test_quest.id, self.test_answer.id)
        data = {'username': 'testuser',
                'email': 'testuser@email.com',
                'password': 'testpassword'
                }

        # 401 UNAUTHORIZED
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # 202 ACCEPT
        response = self.client.post('/user/signup', data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + response.data.get('token'))
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Answer.objects.get(id=self.test_answer.id).votes_count, 1)
        self.assertEqual(Question.objects.get(id=self.test_quest.id).total_votes, 1)
        user = User.objects.get(username=data.get('username'))
        self.assertIn(self.test_quest, user.userprofile.voted_posts.all())

        # 404 NOT FOUND
        response = self.client.post('/user/votefor/666/answer/666/', {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
