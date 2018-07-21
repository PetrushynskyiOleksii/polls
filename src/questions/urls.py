"""Questions' URL Configuration."""

from django.urls import path
from rest_framework import routers
from .views import QuestionViewSet, votefor, AnswerViewSet

router = routers.SimpleRouter()
router.register(r'', QuestionViewSet)
router.register(r'(?P<question_pk>\d+)', AnswerViewSet)

urlpatterns = [
    path('<int:question_pk>/votefor/<int:answer_pk>/', votefor),
]

urlpatterns += router.urls
