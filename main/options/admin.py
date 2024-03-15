from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(SaveProject)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user' , 'freelancer' , 'content' , 'is_reply')

@admin.register(RequestFreelancer)
class RequestFreelancerAdmin(admin.ModelAdmin):
    list_display = ('user' , 'project' , 'is_accept')

@admin.register(RequestEmployer)
class RequestEmployerAdmin(admin.ModelAdmin):
    list_display = ('employer' , 'freelancer' , 'is_accept')




