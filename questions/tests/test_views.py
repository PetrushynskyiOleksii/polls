"""Test for views of question app."""

import json

from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from questions.models import Question, Answer


class QuestionListViewTest(TestCase):
    """Test for ListView of question."""

    def setUp(self):
        """Pre-populate test data."""
        self.client = APIClient()
        self.test_first_quest = Question.objects.create(question='test first question')
        self.test_second_quest = Question.objects.create(question='test second question',
                                                         total_votes=2)
        self.test_third_quest = Question.objects.create(question='test third question',
                                                        total_votes=3)
        self.test_first_answer = Answer.objects.create(question=self.test_first_quest,
                                                       answer='test first answer'
                                                       )

    def tearDown(self):
        """Clean-up test data."""
        del self.client
        del self.test_first_quest
        del self.test_second_quest
        del self.test_third_quest
        del self.test_first_answer

    def test_questions_list(self):
        """Test list of questions."""
        response = self.client.get('/question/all/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Question.objects.count())

        response_json = json.dumps(response.data)
        for quest in Question.objects.all():
            self.assertIn(quest.question, response_json)
            self.assertIn(str(quest.total_votes), response_json)
            for ans in Answer.objects.filter(question=quest):
                self.assertIn(ans.answer, response_json)
                self.assertIn(str(ans.votes_count), response_json)


class QuestionCRDViewTest(TestCase):
    """Test for CRDView of question."""

    def setUp(self):
        """Pre-populate test data."""
        self.client = APIClient()

    def tearDown(self):
        """Clean-up test data."""
        del self.client

    def test_question_create_delete_retrieve(self):
        """Test create question."""
        data = {'question': 'test question',
                'answers': [
                            {'answer': 'first answer'},
                            {'answer': 'second answer'}
                            ]
                }

        # ----- Create -------
        response = self.client.post('/question/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)
        quest = Question.objects.get(question='test question')
        self.assertIsNotNone(quest)
        self.assertEqual(quest.total_votes, 0)

        data.pop('answers')
        response = self.client.post('/question/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # ----- Retrieve -----
        response = self.client.get('/question/{}/'.format(quest.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = json.dumps(response.data)
        self.assertTrue(quest.question in response_json)
        self.assertTrue(str(quest.total_votes) in response_json)

        response = self.client.get('/question/100/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # ----- Delete -------
        response = self.client.delete('/question/{}/'.format(quest.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Question.DoesNotExist):
            Question.objects.get(id=quest.id)

        response = self.client.delete('question/100/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
