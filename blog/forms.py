from django.forms import ModelForm, widgets
from django import forms
from .models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        
