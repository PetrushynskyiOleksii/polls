"""Users' URL Configuration."""

from django.conf.urls import url
from .views import ListCreateQuestion, QuestionRetrieveDestroy

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', QuestionRetrieveDestroy.as_view()),
    url(r'^create/$', ListCreateQuestion.as_view()),
    url(r'^all/$', ListCreateQuestion.as_view()),
]
