from django.db import models
from django.contrib.auth.models import User

# Create your models here.
User._meta.get_field('email')._unique = True


class Feedback(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=150)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name
    
    
class Image(models.Model):
    phrase = models.CharField(max_length=200)
    ai_image = models.ImageField(upload_to="images")
    
    def __str__(self):
        return str(self.phrase)