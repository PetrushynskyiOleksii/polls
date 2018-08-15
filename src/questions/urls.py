"""Questions' URL Configuration."""

from django.urls import path
from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'', views.QuestionViewSet)
router.register(r'(?P<question_pk>\d+)', views.AnswerViewSet)

urlpatterns = [
    path('top/', views.TopQuestions.as_view()),
    path('<int:question_pk>/votefor/<int:answer_pk>/', views.votefor),
]

urlpatterns += router.urls
