"""Test for views of users' app."""

from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_jwt.settings import api_settings

from questions.models import Answer, Question

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserVoteTest(TestCase):
    """Test for API user's votes views."""

    def setUp(self):
        """Pre-populate test data."""
        self.client = APIClient()
        self.testuser = User.objects.create(username='user',
                                            email='user@gmail.com',
                                            password='testpassword')
        self.test_quest = Question.objects.create(question='test question', user=self.testuser)
        self.test_answer = Answer.objects.create(question=self.test_quest, answer='test answer')

    def tearDown(self):
        """Clean-up test data."""
        del self.client
        del self.testuser
        del self.test_quest
        del self.test_answer

    def test_vote_views(self):
        """Test vote views."""
        url = '/question/{}/votefor/{}/'.format(self.test_quest.id, self.test_answer.id)
        data = {'username': 'testuser',
                'email': 'testuser@email.com',
                'password': 'testpassword'
                }
        response = self.client.post('/user/signup', data, format='json')
        token = response.data.get('token')

        # 401 UNAUTHORIZED
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # 202 ACCEPT
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Answer.objects.get(id=self.test_answer.id).votes_count, 1)
        self.assertEqual(Question.objects.get(id=self.test_quest.id).total_votes, 1)
        user = User.objects.get(username=data.get('username'))
        self.assertIn(self.test_quest, user.userprofile.voted_posts.all())

        # 404 NOT FOUND
        response = self.client.post('/user/votefor/666/answer/666/', {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
