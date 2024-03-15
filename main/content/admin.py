from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Category)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('user','title','status','complete')
    prepopulated_fields = {'slug':('title',)}


