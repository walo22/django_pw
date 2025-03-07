#from typing import Any
from django.contrib import admin
from django.db.models import Count
from django.http import HttpRequest
from . import models

# Register your models here.


admin.site.register(models.Category)





@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title' , 'status', 'user' , 'category', 'created_at', 'tasks_count']
    list_per_page =20
    #list_display_page =20
    list_editable = ['status']
    list_celect_related = ['category', 'user']
    #list_display_related = ['category', 'user']



    def tasks_count(self, obj):
        #return obj.task_set.count()
        return obj.tasks_count
    

    def get_queryset(self, request):
        query = super().get_queryset(request)
        query = query.annotate(tasks_count=Count('task'))
        return query




@admin.register(models.Task) 
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id' , 'description', 'project' , 'is_completed']
    list_editable = ['is_completed']
    list_per_page =20