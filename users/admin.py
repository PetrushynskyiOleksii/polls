"""Management admin panel of users' app."""

from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.models import User

from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    """Additional fields to Order on admin page."""

    model = UserProfile
    extra = 0


class UserAdmin(auth_admin.UserAdmin):
    """Class that represents users at admin page."""

    inlines = [UserProfileInline]
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ['username', 'email', 'is_staff', 'is_active']


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
