"""Test for views of question app."""

from django.test import TestCase
from django.contrib.auth.models import User

from questions.models import Question, Answer


class AnswerSignalsTest(TestCase):
    """Test signals of answer model."""

    def setUp(self):
        """Pre-populate test data."""
        self.testuser = User.objects.create(username='testuser',
                                            email='testuser@gmail.com',
                                            password='testpassword')
        self.test_question = Question.objects.create(question='test question',
                                                     total_votes=2,
                                                     user=self.testuser)
        self.test_answer = Answer.objects.create(question=self.test_question,
                                                 answer='test answer',
                                                 votes_count=2)

    def tearDown(self):
        """Clean-up test data."""
        del self.testuser
        del self.test_question
        del self.test_answer

    def test_post_delete_signal(self):
        """Test total votes of question after remove answer."""
        answer = Answer.objects.get(id=self.test_answer.id)
        total_votes = self.test_question.total_votes
        answer.delete()
        question = Question.objects.get(id=self.test_question.id)
        self.assertNotEqual(total_votes, question.total_votes)
        self.assertEqual(question.total_votes, total_votes - self.test_answer.votes_count)

    def test_post_save_signal(self):
        """Test total votes of question after vote for answer."""
        answer = Answer.objects.get(id=self.test_answer.id)
        total_votes = self.test_question.total_votes
        answer.votes_count += 1
        answer.save()
        question = Question.objects.get(id=self.test_question.id)
        self.assertNotEqual(total_votes, question.total_votes)
        self.assertEqual(question.total_votes, total_votes + 1)
