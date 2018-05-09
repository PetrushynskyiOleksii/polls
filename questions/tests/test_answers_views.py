"""Test for views of question app."""

from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from questions.models import Question, Answer


class AnswerViewsTest(TestCase):
    """Test for API ListView of question."""

    def setUp(self):
        """Pre-populate test data."""
        self.client = APIClient()
        self.test_question = Question.objects.create(question='test question')

    def tearDown(self):
        """Clean-up test data."""
        del self.client
        del self.test_question

    def test_create_delete_views(self):
        """Test list of questions."""
        # ----- Create -----
        data = {'answer': 'first answer'}
        url = '/question/{}/answer/create/'.format(self.test_question.id)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        answer = Answer.objects.get(question=self.test_question,
                                    id=int(response.data.get('id')))
        self.assertEqual(answer.votes_count, 0)

        url = '/question/{}/answer/create/'.format(self.test_question.id)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'answer': ''}
        url = '/question/{}/answer/create/'.format(self.test_question.id)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # ----- Delete -------
        url = '/question/{}/answer/{}/'.format(self.test_question.id, answer.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Answer.DoesNotExist):
            Answer.objects.get(id=answer.id)

        response = self.client.delete('question/100/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
