from django.contrib import admin
from webapp.models import Task, Type, Status

# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'description', 'created_at', 'updated_at', 'status_key', 'type_key']
    fields = ['id', 'summary', 'description', 'status_key', 'type_key']
    readonly_fields = ['created_at', 'updated_at', 'id']


admin.site.register(Task, TaskAdmin)
admin.site.register(Type)
admin.site.register(Status)
