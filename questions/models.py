"""Models of questions' app."""

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


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


@receiver(post_delete, sender=Answer)
def update_total_votes(sender, instance, **kwargs):
    """Subtract votes count of removed answer from total count of votes."""
    question = instance.question
    question.total_votes = question.total_votes - instance.votes_count
    question.save()
