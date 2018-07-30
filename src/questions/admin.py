"""Management admin panel of questions' app."""

from django.contrib import admin

from .models import Question, Answer


class AnswerInline(admin.TabularInline):
    """Additional fields to Question on admin page."""

    model = Answer
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Class that represents question at admin page."""

    inlines = [AnswerInline]
    list_display = ('id', 'question', 'total_votes', )
    list_filter = ('total_votes', 'user', )
    search_fields = ['id', ' question', 'user']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Class that represents answer at admin page."""

    list_display = ('id', 'answer', 'question', 'votes_count',)
    list_filter = ('question',)
    search_fields = ['id', 'question', 'answer']
