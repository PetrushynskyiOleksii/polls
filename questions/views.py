"""Views for questions' app."""

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import (ListAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     CreateAPIView,
                                     )

from .models import Question, Answer
from .serializers import QuestionSerializer
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


@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def votefor(request, quest, pk):
    """Create a vote to the corresponding answer."""
    user = request.user
    try:
        answer = Answer.objects.get(id=pk)
        question = Question.objects.get(id=quest)
    except ObjectDoesNotExist:
        return Response({'status': 'failed',
                         'detail': 'doesn\'t exist given answer or question'},
                        status=status.HTTP_404_NOT_FOUND)

    if question not in user.userprofile.voted_posts.all():
        user.userprofile.voted_posts.add(question)
        answer.votes_count += 1
        answer.save()
    else:
        return Response({'status': 'failed',
                         'detail': 'already voted'},
                        status=status.HTTP_400_BAD_REQUEST)

    return Response({'status': 'sucess'},
                    status=status.HTTP_202_ACCEPTED)
