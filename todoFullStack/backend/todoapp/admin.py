from django.contrib import admin

# Register your models here.
from .models import TodoModel

class TodoAdmin(admin.ModelAdmin):
    list_display= [
        "title",
        "body",
        "createdAt",
        "isCompleted",
    ]
admin.site.register(TodoModel, TodoAdmin)