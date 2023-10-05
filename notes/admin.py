from django.contrib import admin
from .models import Note, Report


# admin.site.register(Note)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['pk', 'author', 'title', 'created_at']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['pk', 'author', 'file', 'read', 'created_at']
