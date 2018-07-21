"""Test for answers views of question app."""

import json

from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from questions.models import Question, Answer
from rest_framework_jwt.serializers import User


class AnswerRetriveUpdateDeleteViewTest(TestCase):
    """Test class for retrieve, update, delete answer views."""

    def setUp(self):
        """Pre-populate test data."""
        self.client = APIClient()
        user_data = {'username': 'testuser', 'email': 'testuser@email.com', 'password': 'testpassword'}
        response = self.client.post('/user/signup', user_data, format='json')
        self.user = User.objects.get(username=user_data.get('username'))
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + response.data.get('token'))

        self.question = Question.objects.create(user=self.user, question='test question')
        self.answer = Answer.objects.create(question=self.question, answer='test answer')
        self.url = f'/question/{self.question.id}/{self.answer.id}/'
        self.bad_url = f'/question/{self.question.id}{999}/'

    def tearDown(self):
        """Clean-up test data."""
        del self.client
        del self.question
        del self.answer
        del self.url
        del self.bad_url

    def test_retrieve_view(self):
        """Test retrieve view for answers."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = json.dumps(response.data)
        self.assertIn(str(self.answer.id), response_json)
        self.assertIn(self.answer.answer, response_json)
        self.assertIn(str(self.answer.votes_count), response_json)

        response = self.client.get(self.bad_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_view(self):
        """Test update view for answers."""
        update_data = {'answer': 'updated answer'}

        response = self.client.put(self.url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        update_answer = Answer.objects.get(id=self.answer.id)
        self.assertNotEqual(update_answer.answer, self.answer.answer)
        self.assertEqual(update_answer.answer, update_data.get('answer'))
        with self.assertRaises(Answer.DoesNotExist):
            Answer.objects.get(question=self.question, answer=self.answer.answer)

        response_json = json.dumps(response.data)
        self.assertIn(str(update_answer.id), response_json)
        self.assertIn(update_answer.answer, response_json)
        self.assertIn(str(update_answer.votes_count), response_json)

        response = self.client.put(self.bad_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_view(self):
        """Test delete view for answers."""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Answer.DoesNotExist):
            Answer.objects.get(id=self.answer.id)

        response = self.client.delete(self.bad_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_object_level_permission(self):
        """Test object-level permission for delete/update views."""
        user = {'username': 'anotheruser',
                'email': 'anotheruser@email.com',
                'password': 'testpassword'
                }

        response = self.client.post('/user/signup', user, format='json')
        bad_token = response.data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + bad_token)

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.put(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_permission(self):
        """Test auth permission for update/destroy actions."""
        unauth_client = APIClient()

        response = unauth_client.put(self.url, {'answer': 'update answer'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = unauth_client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
