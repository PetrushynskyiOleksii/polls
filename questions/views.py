"""Views for questions' app."""

from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveDestroyAPIView
                                     )

from .models import Question
from .serializers import QuestionSerializer


class ListCreateQuestion(ListCreateAPIView):
    """Create question, show all existing questions."""

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionRetrieveDestroy(RetrieveDestroyAPIView):
    """Retrive, destroy api of question object."""

    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
