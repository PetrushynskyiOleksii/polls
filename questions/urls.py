"""Users' URL Configuration."""

from django.conf.urls import url
from .views import ListCreateQuestion, QuestionRetrieveUpdateDestroy

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', QuestionRetrieveUpdateDestroy.as_view()),
    url(r'^create/$', ListCreateQuestion.as_view()),
    url(r'^all/$', ListCreateQuestion.as_view()),
]
