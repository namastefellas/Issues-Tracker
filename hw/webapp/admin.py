from django.contrib import admin
from webapp.models import Task, Type, Status, Project

# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'description', 'created_at', 'updated_at', 'status_key']
    fields = ['summary', 'description', 'status_key']
    readonly_fields = ['created_at', 'updated_at', 'id']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'started_at', 'end_at']
    fields = ['name', 'description', 'started_at', 'end_at', 'user']


admin.site.register(Task, TaskAdmin)
admin.site.register(Type)
admin.site.register(Status)
admin.site.register(Project, ProjectAdmin)