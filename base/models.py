from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Users(models.Model):
    firstname = models.CharField(max_length=20, null=False, blank=False)
    lastname = models.CharField(max_length=20, null=False, blank=False)
    email = models.EmailField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.firstname
  


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
