"""Models of questions' app."""

from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save


class Question(models.Model):
    """Model that represents question."""

    class Meta:
        """Meta data of question model."""

        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    question = models.CharField(verbose_name='Question',
                                max_length=255)
    total_votes = models.IntegerField(verbose_name='Total Votes',
                                      default=0)
    user = models.ForeignKey(User, verbose_name='Owner')

    def __str__(self):
        """Render the question instance as a string."""
        return self.question


class Answer(models.Model):
    """Model that represents answer."""

    class Meta:
        """Meta data of answer model."""

        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    question = models.ForeignKey(Question,
                                 verbose_name='Question',
                                 related_name='answers',
                                 on_delete=models.CASCADE)
    answer = models.CharField(verbose_name='Answer',
                              blank=True,
                              max_length=255)
    votes_count = models.IntegerField(verbose_name='Count of Votes',
                                      default=0)

    def __str__(self):
        """Render the answer instance as a string."""
        return ('%s (%d)') % (self.answer, self.votes_count)


@receiver(post_save, sender=Answer)
@receiver(post_delete, sender=Answer)
def update_total_votes(sender, instance, **kwargs):
    """Update total votes of question after signals."""
    question = instance.question
    answers = Answer.objects.filter(question=question)
    total_votes = 0
    for ans in answers:
        total_votes += ans.votes_count

    question.total_votes = total_votes
    question.save()
