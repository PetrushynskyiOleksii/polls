"""Serializer for answer&question models."""

from django.db import transaction
from rest_framework import serializers

from .models import Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    """Serializer of answer model."""

    class Meta(object):
        """Meta settings for AnswerSerializer."""

        model = Answer
        fields = ('id', 'answer', 'votes_count')
        read_only_fields = ('votes_count', 'id',)


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer of question model."""

    user = serializers.StringRelatedField()
    answers = AnswerSerializer(many=True)

    class Meta(object):
        """Meta settings for QuestionSerializer."""

        model = Question
        fields = ('id', 'question', 'answers', 'total_votes', 'user')
        read_only_fields = ('id', 'total_votes', )

    def create(self, validated_data):
        """Create question with validate data."""
        answers_data = validated_data.pop('answers')

        with transaction.atomic():
            question = Question.objects.create(**validated_data)
            for answer_data in answers_data:
                Answer.objects.create(question=question, **answer_data)

        return question

    def update(self, instance, validated_data):
        """Update data of question and answers objects."""
        question = Question.objects.get(id=instance.id)

        if 'answers' in validated_data:
            answer_ids_new = []
            answer_ids_pre = instance.answers.all().values_list('id', flat=True)

            # Perform create
            for answer in validated_data.pop('answers'):
                ans, _created = Answer.objects.get_or_create(question=question, **answer)
                ans.question = instance
                ans.save()
                answer_ids_new.append(ans.id)

            # Perform delete
            delete_ids = set(answer_ids_pre) - set(answer_ids_new)
            Answer.objects.filter(id__in=delete_ids).delete()

        for item, value in validated_data.items():
            setattr(instance, item, value)

        instance.save()

        return instance

    def validate_answers(self, answers):
        """Validate count of answers before create question."""
        if len(answers) < 2:
            raise serializers.ValidationError('Require more then 2 answers.')
        return answers
