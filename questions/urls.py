"""Users' URL Configuration."""

from django.conf.urls import url
from .views import (QuestionList,
                    QuestionCreate,
                    QuestionRetrieveUpdateDestroy,
                    AnswerDestroy,
                    AnswerCreate)

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', QuestionRetrieveUpdateDestroy.as_view()),
    url(r'^create/$', QuestionCreate.as_view()),
    url(r'^(?P<quest>[0-9]+)/answer/(?P<pk>[0-9]+)/$', AnswerDestroy.as_view()),
    url(r'^(?P<pk>[0-9]+)/answer/create/$', AnswerCreate.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', QuestionRetrieveUpdateDestroy.as_view()),
    url(r'^all/$', QuestionList.as_view()),
]
