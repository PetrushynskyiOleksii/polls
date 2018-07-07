"""Users' URL Configuration."""

from django.urls import path
from .views import (CreateUserView,
                    LoginUserView
                    )

urlpatterns = [
    path('signup', CreateUserView.as_view()),
    path('login', LoginUserView.as_view()),
]
