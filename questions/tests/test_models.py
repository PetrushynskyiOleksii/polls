"""Tests for models of question app."""

from django.test import TestCase

from questions.models import Question, Answer


class QuestionAnswerModelTest(TestCase):
    """Tests for question and answer model."""

    def setUp(self):
        """Pre-populate test data."""
        self.test_quest = Question.objects.create(question='test question')
        self.test_first_ans = Answer.objects.create(question=self.test_quest,
                                                    answer='first test answer')
        self.test_second_ans = Answer.objects.create(question=self.test_quest,
                                                     answer='second test answer',
                                                     votes_count=2)
        self.test_third_ans = Answer.objects.create(question=self.test_quest,
                                                    answer='third test answer',
                                                    votes_count=3)

    def tearDown(self):
        """Clean-up test data."""
        del self.test_quest
        del self.test_first_ans
        del self.test_second_ans
        del self.test_third_ans

    def test_quest_str(self):
        """Question model is rendered as its question."""
        self.assertEqual(str(self.test_quest), 'test question')

    def test_answer_str(self):
        """Answer model is rendered as its answer with count of votes."""
        self.assertEqual(str(self.test_first_ans), 'first test answer (0)')
        self.assertEqual(str(self.test_second_ans), 'second test answer (2)')
        self.assertEqual(str(self.test_third_ans), 'third test answer (3)')
