"""Views for questions' app."""

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet

from .models import Question, Answer
from .serializers import QuestionSerializer
from .permissions import IsOwnerOrReadOnly


class QuestionViewSet(ModelViewSet):
    """
    Question's view set.

    list:
    Return list of all existing questions.

    create:
    Create a new question instance.

    retrieve:
    Return the question instance which has id = `id`.

    update:
    Update the question instance which has id = `id`.

    destroy:
    Destroy the question instance which has id = `id`.
    """

    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    filter_backends = (OrderingFilter,)
    ordering = ('-total_votes',)

    def get_permissions(self):
        """Instantiate and return the list of permissions."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['destroy', 'update']:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Create a new question instance."""
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """Update question with given data."""
        serializer.save(user=self.request.user)


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
