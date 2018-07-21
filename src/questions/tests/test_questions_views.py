"""Test for question views of question app."""

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
        self.testuser = User.objects.create(username='testuser', email='testuser@gmail.com',
                                            password='testpassword')
        self.test_first_quest = Question.objects.create(question='test first question',
                                                        user=self.testuser)
        self.test_second_quest = Question.objects.create(question='test second question',
                                                         total_votes=2, user=self.testuser)
        self.test_third_quest = Question.objects.create(question='test third question',
                                                        total_votes=3, user=self.testuser)
        self.test_first_answer = Answer.objects.create(question=self.test_first_quest,
                                                       answer='test first answer')

    def tearDown(self):
        """Clean-up test data."""
        del self.client
        del self.testuser
        del self.test_first_quest
        del self.test_second_quest
        del self.test_third_quest
        del self.test_first_answer

    def test_questions_list(self):
        """Test list view for questions."""
        response = self.client.get('/question/')
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
    """Test for CRUD API view of question."""

    def setUp(self):
        """Pre-populate test data."""
        self.client = APIClient()
        user_data = {'username': 'testuser', 'email': 'testuser@email.com', 'password': 'testpassword'}
        response = self.client.post('/user/signup', user_data, format='json')
        self.user = User.objects.get(username=user_data.get('username'))
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + response.data.get('token'))

        self.question = Question.objects.create(user=self.user, question='test question')
        self.first_answer = Answer.objects.create(question=self.question, answer='test first answer')
        self.second_answer = Answer.objects.create(question=self.question, answer='test second answer')
        self.url = f'/question/{self.question.id}/'
        self.bad_url = f'/question/999/'

    def tearDown(self):
        """Clean-up test data."""
        del self.client
        del self.user
        del self.question
        del self.first_answer
        del self.second_answer

    def test_create_view(self):
        """Test create view for question."""
        create_data = {'question': 'test create question',
                       'answers': [{'answer': 'first answer'}, {'answer': 'second answer'}]}

        # CREATED
        response = self.client.post('/question/', create_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_question = Question.objects.get(id=int(response.data.get('id')))

        self.assertIsNotNone(created_question)
        self.assertEqual(created_question.total_votes, 0)
        self.assertEqual(Answer.objects.filter(question=created_question).count(), 2)
        self.assertIsNotNone(Answer.objects.get(question=created_question, answer='first answer'))
        self.assertIsNotNone(Answer.objects.get(question=created_question, answer='second answer'))
        self.assertEqual(str(User.objects.get(username=self.user.username)), response.data.get('user'))

        response_json = json.dumps(response.data)
        self.assertIn(created_question.question, response_json)
        self.assertIn(str(created_question.total_votes), response_json)
        for ans in Answer.objects.filter(question=created_question):
            self.assertIn(ans.answer, response_json)
            self.assertIn(str(ans.votes_count), response_json)

        # BAD REQUESTS
        bad_data = {'question': 'test question with same answers',
                    'answers': [{'answer': 'same answer'}, {'answer': 'same answer'}]}
        response = self.client.post('/question/', bad_data, format='json')
        self.assertTrue(response.exception)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        bad_data.pop('answers')
        response = self.client.post('/question/', bad_data, format='json')
        self.assertTrue(response.exception)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_view(self):
        """Test update view for question."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_json = json.dumps(response.data)
        self.assertIn(self.question.question, response_json)
        self.assertIn(str(self.question.total_votes), response_json)
        for ans in Answer.objects.filter(question=self.question):
            self.assertIn(str(ans.id), response_json)
            self.assertIn(ans.answer, response_json)
            self.assertIn(str(ans.votes_count), response_json)

        response = self.client.get(self.bad_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_view(self):
        """Test delete view for question."""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Question.DoesNotExist):
            Question.objects.get(id=self.question.id)
        self.assertFalse(Answer.objects.filter(question=self.question).exists())

        response = self.client.delete(self.bad_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_view(self):
        """Test update view for question."""
        update_data = {'question': 'test upd question',
                       'answers': [{'answer': 'first upd answer'}, {'answer': 'second upd answer'}],
                       }

        # UPDATED
        response = self.client.put(self.url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        upd_question = Question.objects.get(id=self.question.id)
        self.assertEqual(upd_question.question, update_data.get('question'))
        with self.assertRaises(Question.DoesNotExist):
            Question.objects.get(question=self.question.question)
        self.assertIsNotNone(Answer.objects.get(question=self.question.id, answer='first upd answer'))
        self.assertIsNotNone(Answer.objects.get(question=self.question.id, answer='second upd answer'))
        with self.assertRaises(Answer.DoesNotExist):
            Answer.objects.get(question=self.question.id, answer=self.first_answer.answer)
            Answer.objects.get(question=self.question.id, answer=self.second_answer.answer)

        response_json = json.dumps(response.data)
        self.assertIn(upd_question.question, response_json)
        self.assertIn(str(upd_question.total_votes), response_json)
        for ans in Answer.objects.filter(question=upd_question):
            self.assertIn(ans.answer, response_json)
            self.assertIn(str(ans.votes_count), response_json)

        # BAD REQUESTS
        bad_data = {'question': 'test question with same answers',
                    'answers': [{'answer': 'same answer'}, {'answer': 'same answer'}]}
        response = self.client.put(self.url, bad_data, format='json')
        self.assertTrue(response.exception)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        bad_data.pop('answers')
        response = self.client.put(self.url, bad_data, format='json')
        self.assertTrue(response.exception)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_auth_permission(self):
        """Test auth permission for update/destroy actions."""
        unauth_client = APIClient()

        response = unauth_client.put(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = unauth_client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_object_level_permission(self):
        """Test object-level permission for update/delete views of question model."""
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
