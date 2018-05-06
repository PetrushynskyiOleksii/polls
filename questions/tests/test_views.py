"""Test for views of question app."""

from rest_framework import status

from django.test import TestCase, Client

from questions.models import Question, Answer


class QuestionViewTest(TestCase):
    """Test for post views."""

    def setUp(self):
        """Pre-populate test data."""
        self.client = Client()
        self.test_first_quest = Question.objects.create(question='test first question')
        self.test_second_quest = Question.objects.create(question='test second question')

        self.test_first_ans = Answer.objects.create(question=self.test_first_quest,
                                                    answer='first test answer')
        self.test_second_ans = Answer.objects.create(question=self.test_first_quest,
                                                     answer='second test answer',
                                                     votes_count=2)
        self.test_third_ans = Answer.objects.create(question=self.test_first_quest,
                                                    answer='third test answer',
                                                    votes_count=3)

    def tearDown(self):
        """Clean-up test data."""
        del self.client
        del self.test_first_quest
        del self.test_second_quest

        del self.test_first_ans
        del self.test_second_ans
        del self.test_third_ans

    def test_questions_list(self):
        """Test list of questions."""
        response = self.client.get('/question/all/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_question_crud(self):
        """Test create question."""
        data = {'question': 'test third question'}
        response = self.client.post('/question/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 3)
        self.assertEqual(Question.objects.get(id=3).question, 'test third question')

        response = self.client.get('/question/3/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('question'), 'test third question')

        response = self.client.get('/question/100/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.delete('/question/3/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Question.objects.filter(id=3).first(), None)

        response = self.client.delete('question/3/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
