"""Users' URL Configuration."""

from django.conf.urls import url

from .views import (CreateUserView,
                    LoginUserView,
                    votefor)

urlpatterns = [
    url(r'^signup', CreateUserView.as_view()),
    url(r'^login', LoginUserView.as_view()),
    url(r'^votefor/(?P<quest>[0-9]+)/answer/(?P<pk>[0-9]+)/$', votefor),
]
