"""Serializer for users' models."""

from rest_framework import serializers

from .models import Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    """Serialize answer model."""

    votes_count = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField()

    class Meta(object):
        """Meta settings for AnswerSerializer."""

        model = Answer
        fields = ('id', 'answer', 'votes_count')

    def create(self, validated_data):
        """Create answer."""
        return Answer.objects.create(**validated_data)


class QuestionSerializer(serializers.ModelSerializer):
    """Serialize question model."""

    total_votes = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField()
    answers = AnswerSerializer(many=True)

    class Meta(object):
        """Meta settings for QuestionSerializer."""

        model = Question
        fields = ('id', 'question', 'answers', 'total_votes', 'user')

    def create(self, validated_data):
        """Create question."""
        answers_data = validated_data.pop('answers')
        question = Question.objects.create(**validated_data)
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)

        return question

    def update(self, instance, validated_data):
        """Update question."""
        instance.question = validated_data.get('question', instance.question)
        instance.save()

        question = Question.objects.get(id=instance.id)
        Answer.objects.filter(question=question).delete()

        answers_data = validated_data.pop('answers')
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)

        return instance

    def validate_answers(self, answers):
        """Validate answers field before create question."""
        if len(answers) < 2:
            raise serializers.ValidationError('Require more then 2 answers.')
        return answers
