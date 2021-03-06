"""Test for views of users' app."""

from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_jwt.settings import api_settings

from questions.models import Answer, Question

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class VoteTest(TestCase):
    """Test for API votes views."""

    def setUp(self):
        """Pre-populate test data."""
        self.client = APIClient()

        user_data = {'username': 'testuser', 'email': 'testuser@email.com', 'password': 'testpassword'}
        response = self.client.post('/user/signup', user_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + response.data.get('token'))
        self.user = User.objects.get(username=user_data.get('username'))

        self.question = Question.objects.create(user=self.user, question='test question')
        self.answer = Answer.objects.create(question=self.question, answer='test answer')

    def tearDown(self):
        """Clean-up test data."""
        del self.client
        del self.user
        del self.question
        del self.answer

    def test_vote_view(self):
        """Test vote view with URL that create manually."""
        # ACCEPTED
        response = self.client.post(f'/question/{self.question.id}/votefor/{self.answer.id}/', {})
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Answer.objects.get(id=self.answer.id).votes_count, 1)
        self.assertEqual(Question.objects.get(id=self.question.id).total_votes, 1)
        self.assertIn(self.question, self.user.userprofile.voted_posts.all())

        # UNAUTHORIZED
        unauth_client = APIClient()
        response = unauth_client.post(f'/question/{self.question.id}/votefor/{self.answer.id}/', {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # NOT FOUND
        response = self.client.post(f'/user/votefor/{self.question.id}/answer/999/', {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_autogenerated_vote_url(self):
        """Test URL for vote that autogenerated by serializer."""
        answer_response = self.client.get(f'/question/{self.question.id}/{self.answer.id}/')
        vote_url = answer_response.data.get('vote_url')

        response = self.client.post(vote_url, {})
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Answer.objects.get(id=self.answer.id).votes_count, 1)
        self.assertEqual(Question.objects.get(id=self.question.id).total_votes, 1)
        self.assertIn(self.question, self.user.userprofile.voted_posts.all())
