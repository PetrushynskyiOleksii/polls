"""Users' URL Configuration."""

from django.conf.urls import url
from .views import (QuestionList,
                    QuestionCreate,
                    QuestionRetrieveUpdateDestroy,
                    votefor)

urlpatterns = [
    url(r'^(?P<quest>[0-9]+)/votefor/(?P<pk>[0-9]+)/$', votefor),
    url(r'^create/$', QuestionCreate.as_view()),
    url(r'^all/$', QuestionList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', QuestionRetrieveUpdateDestroy.as_view()),
]
