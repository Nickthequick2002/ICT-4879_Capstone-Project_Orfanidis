from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Blog model that handles the blogs behavior
class Blog(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=250, blank=True)  
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
