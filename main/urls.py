"""Polls URL configuration."""

from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^question/', include('questions.urls', namespace='questions')),
]
