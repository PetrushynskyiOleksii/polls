"""Models of questions' app."""

from django.db import models
from django.db.models import Sum
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save


class QuestionManager(models.Manager):
    """Custom manager for question model."""

    def all_with_related_fields(self):
        """Query questions with related fields."""
        qs = Question.objects.select_related('user').only(
            'user__username', 'question', 'total_votes'
        )
        qs = qs.prefetch_related('answers')

        return qs

    def top_questions(self, limit=10):
        """Return top [limit] popular questions."""
        qs = Question.objects.all_with_related_fields()
        qs = qs.order_by('-total_votes')[:limit]

        return qs


class Question(models.Model):
    """Model that represents question information."""

    class Meta:
        """Meta settings of question model."""

        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    question = models.CharField(verbose_name='Question', max_length=255, unique=True)
    total_votes = models.IntegerField(verbose_name='Total Votes', default=0, null=True)
    user = models.ForeignKey(User, verbose_name='Owner', on_delete=models.CASCADE)

    objects = QuestionManager()

    def __str__(self):
        """Render the question instance as a string."""
        return self.question


class AnswerManager(models.Manager):
    """Custom manager for answer model."""

    def all_with_related_question_owner(self):
        """Query answers with all related fields."""
        qs = Answer.objects.select_related('question__user').only(
            'answer', 'votes_count', 'question__user'
        )
        return qs


class Answer(models.Model):
    """Model that represents answer information."""

    class Meta:
        """Meta settings of answer model."""

        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
        unique_together = ('question', 'answer',)

    question = models.ForeignKey(Question, verbose_name='Question', related_name='answers',
                                 on_delete=models.CASCADE)
    answer = models.CharField(verbose_name='Answer', blank=True, max_length=255)
    votes_count = models.IntegerField(verbose_name='Count of Votes', default=0)

    objects = AnswerManager()

    def __str__(self):
        """Render the answer instance as a string."""
        return f'{self.answer} ({self.votes_count})'


@receiver(post_save, sender=Answer)
@receiver(post_delete, sender=Answer)
def update_total_votes(sender, instance, **kwargs):
    """Update total votes of question after signals."""
    question = instance.question
    question_answers = sender.objects.filter(question=question).aggregate(total_votes=Sum('votes_count'))
    question.total_votes = question_answers.get('total_votes', 0)
    question.save(update_fields=('total_votes',))
