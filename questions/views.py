"""Views for questions' app."""

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     DestroyAPIView,
                                     CreateAPIView,
                                     )

from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer


class ListCreateQuestion(ListCreateAPIView):
    """Create question, show all existing questions."""

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    """Retrive, destroy api of question object."""

    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class AnswerDestroy(DestroyAPIView):
    """Delete API view for Answer model."""

    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()


class AnswerCreate(CreateAPIView):
    """Create API view for Answer model."""

    serializer_class = AnswerSerializer

    def create(self, request, pk):
        """Create answer with given data for question(id=pk)."""
        question = Question.objects.get(id=pk)
        answer_data = request.data.get('answer')

        if len(answer_data) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        answer, created = Answer.objects.get_or_create(question=question, answer=answer_data)
        serializer = self.serializer_class(answer)
        if created:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
