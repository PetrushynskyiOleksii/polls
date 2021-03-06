"""Polls URL configuration."""

from django.contrib import admin
from django.conf.urls import include
from django.urls import path

from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import (obtain_jwt_token,
                                      verify_jwt_token,
                                      refresh_jwt_token
                                      )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include_docs_urls(title='API of vote app.')),

    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('api-token-verify/', verify_jwt_token),

    path('question/', include('questions.urls')),
    path('user/', include('users.urls')),
]
