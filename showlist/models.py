from django.db import models
from django.contrib.auth.models import User



class TodoItem (models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True)    
    content = models.TextField()
    added_time = models.DateTimeField(auto_now=True)


