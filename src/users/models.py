"""Models of users' app."""

from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from questions.models import Question


class UserProfile(models.Model):
    """Extra user data (profile)."""

    class Meta(object):
        """Meta settings for user profile."""

        verbose_name = 'User Profile'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    voted_posts = models.ManyToManyField(Question, verbose_name='Voted questions')

    def __str__(self):
        """Return the profile instance as a string."""
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create profile for new user."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Update profile after signal from user model."""
    instance.userprofile.save()
