from django.forms import ModelForm
from .models import Users, Post
from django import forms
from .models import Post


class UserForm(ModelForm):
    class Meta:
        model = Users
        fields = ('firstname','lastname','email')
        
        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        
            
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'author']
