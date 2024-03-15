from typing import Any, Optional
from django.contrib import admin

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *
from .forms import *
# Register your models here.

admin.site.register(Skill)

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['username','email','status','is_admin']
    list_filter = ['status',]
    search_fields = ('username',)
    filter_horizontal = ('groups' , 'user_permissions')
    ordering =('username',)

    fieldsets = (
        ('Account User',{'fields':('phone','email','username','status','skills','password')}),
        ('User Permissions',{'fields':('is_active','is_admin','is_superuser','groups','user_permissions')}),
    )

    add_fieldsets = (
        ('Create Account',{'fields':('phone','email','username','status','skills','password1','password2')}),
    )

    def get_form(self, request, obj = None, **kwargs) :
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form



admin.site.register(User,UserAdmin)

admin.site.register(OTP)
admin.site.register(UserProfile)
admin.site.register(City)
admin.site.register(UserEmployerProfile)

