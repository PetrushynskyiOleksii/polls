"""Views for questions' app."""

from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import (ListAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     DestroyAPIView,
                                     CreateAPIView,
                                     )

from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer
from .permissions import IsOwnerOrReadOnly


class QuestionList(ListAPIView):
    """Show all existing questions."""

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionCreate(CreateAPIView):
    """Create API view for Question model."""

    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionSerializer

    def create(self, request, **kwargs):
        """Create question with given data."""
        user = User.objects.get(username=request.user)
        request.data['user'] = user.id
        return super(QuestionCreate, self).create(request, **kwargs)


class QuestionRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    """Retrive, destroy, update API of question object."""

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, )
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def update(self, request, **kwargs):
        """Update question with given data."""
        user = User.objects.get(username=request.user)
        request.data['user'] = user.id
        return super(QuestionRetrieveUpdateDestroy, self).update(request, **kwargs)


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
