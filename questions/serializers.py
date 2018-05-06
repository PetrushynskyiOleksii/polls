"""Serializer for users' models."""

from rest_framework import serializers
from .models import Question, Answer


class QuestionSerializer(serializers.ModelSerializer):
    """Serialize question model."""

    total_votes = serializers.ReadOnlyField()

    class Meta(object):
        """Meta settings for QuestionSerializer."""

        model = Question
        fields = ('question', 'total_votes')


class AnswerSerializer(serializers.ModelSerializer):
    """Serialize answer model."""

    class Meta(object):
        """Meta settings for AnswerSerializer."""

        model = Answer
        fields = ('answer', 'votes_count')
