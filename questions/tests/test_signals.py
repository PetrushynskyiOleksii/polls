"""Test for views of question app."""

from django.test import TestCase

from questions.models import Question, Answer


class AnswerSignalsTest(TestCase):
    """Test signals of answer model."""

    def setUp(self):
        """Pre-populate test data."""
        self.test_question = Question.objects.create(question='test question',
                                                     total_votes=2)
        self.test_answer = Answer.objects.create(question=self.test_question,
                                                 answer='test answer',
                                                 votes_count=2)

    def tearDown(self):
        """Clean-up test data."""
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
