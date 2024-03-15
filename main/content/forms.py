from django import forms

from .models import Project


class ContactUsForm (forms.Form):

    SUBJECT = [
        ('Suport','Suport'),
        ('Questions','Questions'),
        ('Offers','Offers')
    ]

    phone = forms.CharField(max_length=11 , required=False,label='phone')
    email = forms.EmailField(label='email')
    subject = forms.ChoiceField(choices=SUBJECT)
    message = forms.CharField(widget=forms.Textarea)


class CreateProjectForm(forms.ModelForm):
    class Meta:
        model= Project 
        fields = ('title','time','price','content','category','skills')

class EditProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title','time','price','content','category','skills')

