"""Test for views of question app."""

import json

from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIClient

from questions.models import Question, Answer


class QuestionListViewTest(TestCase):
    """Test for API ListView of question."""

    def setUp(self):
        """Pre-populate test data."""
        self.client = APIClient()
        self.testuser = User.objects.create(username='testuser',
                                            email='testuser@gmail.com',
                                            password='testpassword')
        self.test_first_quest = Question.objects.create(question='test first question',
                                                        user=self.testuser)
        self.test_second_quest = Question.objects.create(question='test second question',
                                                         total_votes=2, user=self.testuser)
        self.test_third_quest = Question.objects.create(question='test third question',
                                                        total_votes=3, user=self.testuser)
        self.test_first_answer = Answer.objects.create(question=self.test_first_quest,
                                                       answer='test first answer'
                                                       )

    def tearDown(self):
        """Clean-up test data."""
        del self.client
        del self.testuser
        del self.test_first_quest
        del self.test_second_quest
        del self.test_third_quest
        del self.test_first_answer

    def test_questions_list(self):
        """Test list of questions."""
        response = self.client.get('/question/all/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 3)

        response_json = json.dumps(response.data)
        for quest in Question.objects.all():
            self.assertIn(quest.question, response_json)
            self.assertIn(str(quest.total_votes), response_json)
            for ans in Answer.objects.filter(question=quest):
                self.assertIn(ans.answer, response_json)
                self.assertIn(str(ans.votes_count), response_json)


class QuestionCRUDViewsTest(TestCase):
    """Test for CRDView of question."""

    def setUp(self):
        """Pre-populate test data."""
        self.client = APIClient()

    def tearDown(self):
        """Clean-up test data."""
        del self.client

    def test_question_CRUD_views(self):
        """Test create question."""
        user = {'username': 'testuser',
                'email': 'testuser@email.com',
                'password': 'testpassword'
                }

        response = self.client.post('/user/signup', user, format='json')
        token = response.data.get('token')

        # ----- Create -------
        data = {'question': 'test question',
                'answers': [
                            {'answer': 'first answer'},
                            {'answer': 'second answer'}
                            ]
                }

        response = self.client.post('/question/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.post('/question/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)
        quest = Question.objects.get(id=int(response.data.get('id')))
        self.assertIsNotNone(quest)
        self.assertEqual(quest.total_votes, 0)
        self.assertEqual(Answer.objects.filter(question=quest).count(), 2)
        self.assertIsNotNone(Answer.objects.get(question=quest, answer='first answer'))
        self.assertIsNotNone(Answer.objects.get(question=quest, answer='second answer'))
        self.assertEqual(User.objects.get(username='testuser').id, response.data.get('user'))

        data.pop('answers')
        response = self.client.post('/question/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # ----- Retrieve -----
        response = self.client.get('/question/{}/'.format(quest.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = json.dumps(response.data)
        self.assertIn(quest.question, response_json)
        self.assertIn(str(quest.total_votes), response_json)
        for ans in Answer.objects.filter(question=quest):
            self.assertIn(ans.answer, response_json)
            self.assertIn(str(ans.votes_count), response_json)

        response = self.client.get('/question/100/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Object-level permission
        user = {'username': 'anotheruser',
                'email': 'anotheruser@email.com',
                'password': 'testpassword'
                }

        response = self.client.post('/user/signup', user, format='json')
        bad_token = response.data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + bad_token)

        response = self.client.delete('/question/{}/'.format(quest.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.put('/question/{}/'.format(quest.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # ----- Update -------
        data = {'question': 'test update question',
                'answers': [
                            {'answer': 'first update answer'},
                            {'answer': 'second update answer'}
                            ],
                }

        self.client = APIClient()
        response = self.client.put('/question/{}/'.format(quest.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.put('/question/{}/'.format(quest.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        quest = Question.objects.get(id=quest.id)
        self.assertEqual(quest.question, 'test update question')
        with self.assertRaises(Question.DoesNotExist):
            Question.objects.get(question='test question')
        self.assertIsNotNone(Answer.objects.get(question=quest, answer='first update answer'))
        self.assertIsNotNone(Answer.objects.get(question=quest, answer='second update answer'))
        with self.assertRaises(Answer.DoesNotExist):
            Answer.objects.get(answer='first answer')
            Answer.objects.get(answer='second answer')

        response = self.client.put('/question/100/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        data.pop('answers')
        response = self.client.put('/question/{}/'.format(quest.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # ----- Delete -------
        self.client = APIClient()
        response = self.client.put('/question/{}/'.format(quest.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.delete('/question/{}/'.format(quest.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Question.DoesNotExist):
            Question.objects.get(id=quest.id)
        self.assertEqual(len(Answer.objects.filter(question=quest)), 0)

        response = self.client.delete('question/100/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
