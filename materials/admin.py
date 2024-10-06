from django.contrib import admin

from materials.models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
