from django.forms import ModelForm
from . models import Users, Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


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
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full h-12 px-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-600 bg-teal-100'}),
            'content': forms.Textarea(attrs={'class': 'w-full h-32 px-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-600 bg-teal-100'}),
        }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']