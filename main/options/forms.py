from django import forms

from .models import Comment , RequestEmployer
from content.models import Project

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class ReplyCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class UpdateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)


class RecruitmentForm(forms.ModelForm):
    class Meta:
        model = RequestEmployer
        fields = ('content',)







