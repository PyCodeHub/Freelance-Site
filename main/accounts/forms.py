from typing import Any
from django import forms

from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import *

class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField()
    password2 = forms.CharField()
    
    class Meta:
        model = User
        fields = ('phone' , 'email' , 'username' , 'status' ,'skills')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('Passwords in not Match!')
        return cd['password2']
    
    def save(self, commit= True):
        user =  super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
        

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = User
        fields = ('phone' , 'email' , 'username' , 'status' ,'skills')


# User Register Forms
class UserRegisterForm(forms.Form):

    STATUS = (
        ('Freelancer' , 'Freelancer'),
        ('Employer' , 'Employer'),
        
    )

    status = forms.ChoiceField(choices=STATUS , label='status')
    phone = forms.CharField(max_length=11 , label='phone')

class UserVeryfyCodeForm(forms.Form):
    code = forms.IntegerField(label='code')


class EmployerRegisterForm(forms.Form):
    username = forms.CharField(label='username')
    email = forms.EmailField(label='email')
    password = forms.CharField(label='password')
    password2 = forms.CharField(label='password2')

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username = username).exists()
        if user:
            print('=================Username already exist===============')
            raise ValidationError('Username already exist')
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email = email).exists()
        if user:
            print('=================Email already exist===============')
            raise ValidationError('Email already exist')
        return email
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] and ['password2'] and cd['password'] != cd['password2']:
            print('==============Passwords is not match==============')
            raise ValidationError('Passwords is not match')
        return cd['password2']
    

class FreelancerRegisterForm(forms.ModelForm):
    username = forms.CharField(label='username')
    email = forms.EmailField(label='email')
    password = forms.CharField(label='password')
    password2 = forms.CharField(label='password2')

    class Meta:
        model = User
        fields = ('skills',)
        labels = {
            'skills':'skills'
        }
    
    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username = username).exists()
        if user:
            print('=================Username already exist===============')
            raise ValidationError('Username already exist')
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email = email).exists()
        if user:
            print('=================Email already exist===============')
            raise ValidationError('Email already exist')
        return email
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] and ['password2'] and cd['password'] != cd['password2']:
            print('==============Passwords is not match==============')
            raise ValidationError('Passwords is not match')
        return cd['password2']


# User Login Forms
class UserLoginForm(forms.Form):
    phone = forms.CharField(max_length=11 , label='phone')
    password = forms.CharField(label='password')

class UserLoginVeryfyCodeForm(forms.Form):
    code = forms.IntegerField(label='code')


# Edit Profile User Forms
class EditAccountEmployerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone','email','username')

class EditProfileEmployerForm(forms.ModelForm):
    class Meta:
        model = UserEmployerProfile
        fields = ('image',)


class EditAccountFreelancerForm(forms.ModelForm):
    class Meta:
        model = User
        fields= ('phone','email','username','skills')

class EditProfileFreelancerForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('image','city','about','cv')
