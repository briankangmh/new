from django.contrib import admin
from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'title')
    list_display_links = ('title',)
    search_fields = ('title', 'desc')


admin.site.register(Question, QuestionAdmin)
