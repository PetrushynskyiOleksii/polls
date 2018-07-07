"""Questions' URL Configuration."""

from django.urls import path
from .views import (QuestionList,
                    QuestionCreate,
                    QuestionRetrieveUpdateDestroy,
                    votefor
                    )

urlpatterns = [
    path('all/', QuestionList.as_view()),
    path('create/', QuestionCreate.as_view()),
    path('<int:pk>/', QuestionRetrieveUpdateDestroy.as_view()),
    path('<int:quest>/votefor/<int:pk>/', votefor),
]
