"""Views for users' app."""

import jwt

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer
from main.settings import SECRET_KEY
from questions.models import Answer, Question

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class CreateUserView(CreateAPIView):
    """Create user API view."""

    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        """Create user and return token."""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            user = User.objects.get(username=serializer.data['username'])
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response(
                {'token': token},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginUserView(APIView):
    """Log in user API view."""

    def post(self, request, *args):
        """Log in user and return token."""
        data = request.data
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            payload = jwt_payload_handler(user)
            token = {'token': jwt.encode(payload, SECRET_KEY),
                     'status': 'success'
                     }
            return Response(token, status=status.HTTP_200_OK)
        else:
            token = {'error': 'Invalid credentials',
                     'status': 'failed'
                     }
            return Response(token, status.HTTP_400_BAD_REQUEST)


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
