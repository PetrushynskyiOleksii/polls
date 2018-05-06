"""Views for questions' app."""

from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import Question
from .serializers import QuestionSerializer


class ListCreateQuestion(ListCreateAPIView):
    """Create questions or show all existing questions."""

    queryset = Question.objects.all()

    def list(self, request):
        """Represent all questions."""
        queryset = self.get_queryset()
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create question."""
        data = request.data
        serializer = QuestionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
