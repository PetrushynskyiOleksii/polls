"""Users' URL Configuration."""

from django.conf.urls import url
from .views import (ListCreateQuestion,
                    QuestionRetrieveUpdateDestroy,
                    AnswerDestroy,
                    AnswerCreate)

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', QuestionRetrieveUpdateDestroy.as_view()),
    url(r'^(?P<quest>[0-9]+)/answer/(?P<pk>[0-9]+)/$', AnswerDestroy.as_view()),
    url(r'^(?P<pk>[0-9]+)/answer/create/$', AnswerCreate.as_view()),
    url(r'^create/$', ListCreateQuestion.as_view()),
    url(r'^all/$', ListCreateQuestion.as_view()),
]
