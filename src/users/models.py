"""Models of users' app."""

from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from questions.models import Question


class UserProfile(models.Model):
    """Extra user data."""

    class Meta(object):
        """Meta data for user profile."""

        verbose_name = u'User Profile'

    user = models.OneToOneField(User)
    voted_posts = models.ManyToManyField(Question,
                                         verbose_name=u'Voted questions')

    def __str__(self):
        """Render the user instance as a string."""
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create user profile after create user."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save user profile."""
    instance.userprofile.save()
