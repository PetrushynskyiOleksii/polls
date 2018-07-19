"""Questions' URL Configuration."""

from django.urls import path
from rest_framework import routers
from .views import QuestionViewSet, votefor

router = routers.SimpleRouter()
router.register(r'', QuestionViewSet)

urlpatterns = [
    path('<int:quest>/votefor/<int:pk>/', votefor),
]

urlpatterns += router.urls
